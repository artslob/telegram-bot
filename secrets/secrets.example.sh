#!/usr/bin/env bash

SECRETS_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

token=''
host=''
x_yandex_api_key=''

echo -n "$token" > "${SECRETS_DIR}/token.secret"
echo -n "$host" > "${SECRETS_DIR}/host.secret"
echo -n "$x_yandex_api_key" > "${SECRETS_DIR}/x_yandex_api_key.secret"
