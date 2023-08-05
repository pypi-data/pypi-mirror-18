/*
 * Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
 *
 * This Source Code Form is subject to the terms of the GNU Affero General
 * Public License, v. 3.0. If a copy of the AGPL was not distributed with
 * this file, You can obtain one at https://www.gnu.org/licenses/agpl-3.0.html.
 */
#include "engine.h"

#include <sys/epoll.h>
#include <sys/timerfd.h>
#include <sys/time.h>
#include <unistd.h>

int fm_start(struct fm_queue_t* queue, int interval)
{
    struct itimerspec ts;
    struct epoll_event event;

    queue->td = -1;
    queue->qd = epoll_create(65536);

    if (queue->qd == -1) {
        goto error;
    }

    if (interval > 0 && queue->on_tick) {

        queue->td = timerfd_create(CLOCK_REALTIME, TFD_NONBLOCK);
        if (queue->td == -1) {
            goto error;
        }

        ts.it_interval.tv_sec = interval / 1000000000;
        ts.it_interval.tv_nsec = interval % 1000000000;
        ts.it_value = ts.it_interval;
        if (timerfd_settime(queue->td, 0, &ts, NULL) != 0) {
            goto error;
        }

        event.events = EPOLLIN;
        event.data.ptr = NULL;
        if (epoll_ctl(queue->qd, EPOLL_CTL_ADD, queue->td, &event) != 0) {
            goto error;
        }

    }

    return 0;
error:
    if (queue->td != -1) {
        close(queue->td);
        queue->td = -1;
    }
    if (queue->qd != -1) {
        close(queue->qd);
        queue->qd = -1;
    }
    return -1;
}

int fm_stop(struct fm_queue_t* queue)
{
    int rc = 0;
    int rc2;

    if (queue->td != -1) {
        rc = close(queue->td);
        queue->td = -1;
    }
    if (queue->qd != -1) {
        rc2 = close(queue->qd);
        queue->qd = -1;
        if (rc == 0) {
            rc = rc2;
        }
    }
    return rc;
}

int fm_execute(struct fm_queue_t* queue)
{
    struct epoll_event events[32];
    struct timeval tv;
    int rc;
    int i;

    rc = epoll_wait(queue->qd, events, sizeof(events)/sizeof(events[0]), -1);

    if (rc < 0) {
        return -1;
    }

    if (gettimeofday(&tv, NULL) == -1) {
        return -1;
    }

    for (i = 0; i < rc; i++) {
        if (events[i].data.ptr == NULL) {
            uint64_t count = 0;
            if (read(queue->td, &count, sizeof(count)) != 8) {
                return -1;
            }
            (*queue->on_tick)(queue, &tv, count);
        } else {
            if (events[i].events & EPOLLIN && queue->on_read) {
                (*queue->on_read)(queue, &tv, (struct fm_socket_t*)events[i].data.ptr);
            }
            if (events[i].events & EPOLLOUT && queue->on_write) {
                (*queue->on_write)(queue, &tv, (struct fm_socket_t*)events[i].data.ptr);
            }
        }
    }
    return 0;
}

int fm_attach(struct fm_queue_t* queue, struct fm_socket_t* socket, int events)
{
    socket->events = 0;
    return fm_set_events(queue, socket, events);
}

int fm_detach(struct fm_queue_t* queue, struct fm_socket_t* socket)
{
    return fm_set_events(queue, socket, 0);
}

int fm_set_events(struct fm_queue_t* queue, struct fm_socket_t* socket, int events)
{
    int op;
    struct epoll_event ev;
    int rc;

    events &= FM_EVENT_MASK;
    if (events == socket->events) {
        return 0;
    }

    ev.events = 0;
    if (events & FM_READ) ev.events |= EPOLLIN;
    if (events & FM_WRITE) ev.events |= EPOLLOUT;
    ev.data.ptr = socket;

    if (socket->events == 0) {
        op = EPOLL_CTL_ADD;
    } else if (events == 0) {
        op = EPOLL_CTL_DEL;
    } else {
        op = EPOLL_CTL_MOD;
    }
    rc = epoll_ctl(queue->qd, op, socket->sd, &ev);
    if (rc != -1) {
        socket->events = events;
    }
    return rc;
}

int fm_get_events(struct fm_queue_t* queue, struct fm_socket_t* socket)
{
    return socket->events;
}
