/*
 * Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
 *
 * This Source Code Form is subject to the terms of the GNU Affero General
 * Public License, v. 3.0. If a copy of the AGPL was not distributed with
 * this file, You can obtain one at https://www.gnu.org/licenses/agpl-3.0.html.
 */
#include "engine.h"

#include <sys/types.h>
#include <sys/event.h>
#include <sys/time.h>
#include <unistd.h>

int fm_start(struct fm_queue_t* queue, int interval)
{
    queue->qd = kqueue();

    if (queue->qd == -1) {
        return -1;
    }

    if (interval > 0 && queue->on_tick) {
        struct kevent change;

        EV_SET(&change, 0, EVFILT_TIMER, EV_ADD, NOTE_NSECONDS | NOTE_CRITICAL, interval, NULL);
        if (kevent(queue->qd, &change, 1, NULL, 0, NULL) == -1) {
            close(queue->qd);
            queue->qd = -1;
            return -1;
        }
    }

    return 0;
}

int fm_stop(struct fm_queue_t* queue)
{
    int rc = 0;
    if (queue->qd != -1) {
        rc = close(queue->qd);
        queue->qd = -1;
    }
    return rc;
}

int fm_execute(struct fm_queue_t* queue)
{
    struct kevent events[32];
    struct timeval tv;
    int rc;
    int i;

    rc = kevent(queue->qd, NULL, 0, events, sizeof(events)/sizeof(events[0]), NULL);

    if (rc < 0) {
        return -1;
    }

    if (gettimeofday(&tv, NULL) == -1) {
        return -1;
    }

    for (i = 0; i < rc; i++) {
        switch(events[i].filter) {
            case EVFILT_TIMER:
                (*queue->on_tick)(queue, &tv, events[i].data);
                break;
            case EVFILT_READ:
                if (queue->on_read) {
                    (*queue->on_read)(queue, &tv, (struct fm_socket_t*)events[i].udata);
                }
                break;
            case EVFILT_WRITE:
                if (queue->on_write) {
                    (*queue->on_write)(queue, &tv, (struct fm_socket_t*)events[i].udata);
                }
                break;
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
    struct kevent changes[2];
    int nchanges = 0;
    int flags;
    int rc;

    int diffs = (FM_EVENT_MASK & events) ^ socket->events;
    if (diffs == 0) {
        return 0;
    }
    if (diffs & FM_READ) {
        flags = (events & FM_READ) ? EV_ADD : EV_DELETE;
        EV_SET(changes+nchanges, socket->sd, EVFILT_READ, flags, 0, 0, socket);
        nchanges++;
    }
    if (diffs & FM_WRITE) {
        flags = (events & FM_WRITE) ? EV_ADD : EV_DELETE;
        EV_SET(changes+nchanges, socket->sd, EVFILT_WRITE, flags, 0, 0, socket);
        nchanges++;
    }
    rc = kevent(queue->qd, changes, nchanges, NULL, 0, NULL);
    if (rc != -1) {
        socket->events ^= diffs;
    }
    return rc;
}

int fm_get_events(struct fm_queue_t* queue, struct fm_socket_t* socket)
{
    return socket->events;
}
