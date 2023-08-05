#ifndef __FLOWDAS_METER_ENGINE_H
#define __FLOWDAS_METER_ENGINE_H
/*
 * Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
 *
 * This Source Code Form is subject to the terms of the GNU Affero General
 * Public License, v. 3.0. If a copy of the AGPL was not distributed with
 * this file, You can obtain one at https://www.gnu.org/licenses/agpl-3.0.html.
 */

#include "../../vendor/http-parser/http_parser.h"

#include <stdint.h>

/* socket */
#include <sys/socket.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

#define FM_SOCKET_HEAD \
    int sd;

struct fm_socket_t {
    FM_SOCKET_HEAD
    int events;
};

#define FM_QUEUE_HEAD \
    void *hook;\
    void (*on_tick)(struct fm_queue_t* queue, struct timeval* tv, int count);\
    void (*on_read)(struct fm_queue_t* queue, struct timeval* tv, struct fm_socket_t* socket);\
    void (*on_write)(struct fm_queue_t* queue, struct timeval* tv, struct fm_socket_t* socket);

struct fm_queue_t {
    FM_QUEUE_HEAD
    int qd;
#if FM_EVENT_EPOLL
    int td;
#endif
};

#define FM_READ 1
#define FM_WRITE 2
#define FM_EVENT_MASK (FM_READ|FM_WRITE)

int fm_start(struct fm_queue_t* queue, int interval);
int fm_stop(struct fm_queue_t* queue);
int fm_execute(struct fm_queue_t* queue);
int fm_attach(struct fm_queue_t* queue, struct fm_socket_t* socket, int events);
int fm_detach(struct fm_queue_t* queue, struct fm_socket_t* socket);
int fm_set_events(struct fm_queue_t* queue, struct fm_socket_t* socket, int events);
int fm_get_events(struct fm_queue_t* queue, struct fm_socket_t* socket);

#define EHTTPERROR -1

#endif /* __FLOWDAS_METER_ENGINE_H */
