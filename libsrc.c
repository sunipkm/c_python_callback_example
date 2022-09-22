#include <czmq.h>
#include <stdlib.h>

#define STRLEN 16

typedef void (*cb_func_t)(char *str, size_t len, char *str2, size_t len2);

static void actor_fcn(zsock_t *pipe, void *arg)
{
    cb_func_t cb_fcn = (cb_func_t) arg;
    zpoller_t *poller = zpoller_new(pipe, NULL);
    bool terminated = false;
    static char buf[STRLEN] = {0x0, };
    static char buf2[2 * STRLEN] = {0x0, };
    zsock_signal(pipe, 0);
    while (!terminated)
    {
        void *which = zpoller_wait(poller, 1000); // every second
        if (which == pipe)
        {
            zmsg_t *msg = zmsg_recv(pipe);
            char *cmd = zmsg_popstr(msg);
            if (streq(cmd, "$TERM"))
            {
                terminated = true;
            }
            if (cmd)
                free(cmd);
            zmsg_destroy(&msg);
        }
        else if ((which == NULL) && zpoller_expired(poller))
        {
            if (cb_fcn)
            {
                for (int i = 0; i < STRLEN - 1; i++)
                {
                    buf[i] = (rand() % 26) + 'A' + (rand() % 2 ? 0 : 'a' - 'A');
                }
                buf[STRLEN - 1] = '\0';
                for (int i = 0; i < 2 * STRLEN - 1; i++)
                {
                    buf2[i] = (rand() % 26) + 'A' + (rand() % 2 ? 0 : 'a' - 'A');
                }
                buf2[2 * STRLEN - 1] = '\0';
                cb_fcn(buf, STRLEN, buf2, 2 * STRLEN);
            }
        }
    }
    zpoller_destroy(&poller);
}

zactor_t *actor_new(cb_func_t input)
{
    zactor_t *act = zactor_new(actor_fcn, (void *)input);
    return act;
}

void actor_destroy(void **ptr)
{
    zactor_destroy((zactor_t **)ptr);
}

static void callback_fn(char *ptr, size_t len, char *ptr2, size_t len2)
{
    printf("In callback: %s | %s\n", (char *) ptr, (char *) ptr2);
}

int main()
{
    zactor_t *act = actor_new(callback_fn);
    zclock_sleep(4000);
    actor_destroy((void **)&act);
}