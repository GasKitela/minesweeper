import axios from 'axios'
import humps from 'humps'
import {identity} from "ramda"

const BASE_URI = 'http://localhost:4433';

const api = {
    holaMundo: () =>
        client.get('/hola-mundo'),
    createGame: (game_id, rows, cols, mines) =>
        client.post(`/games/${game_id}/${rows}/${cols}/${mines}`),
    clickSquare: (game_id, rows, cols, action) =>
        client.put(`/games/${game_id}/click/${rows}/${cols}/${action}`),
    getParentFlow: (ticketId, parentFlowId) =>
        client.get(`/aftersale/ajax/hank/tickets/${ticketId}/flows/${parentFlowId}`),
    getEmailPreview: data =>
        client.post("/aftersale/ajax/email-preview/creation", data),
    closeInfoRequest: data =>
        client.post(`/aftersale/ajax/info-request/${data.requestId}/close`, data),
}

const client = (() => {
    const instance = axios.create({
        baseURL: BASE_URI,
        transformResponse: [
            ...axios.defaults.transformResponse,
            data => humps.camelizeKeys(data)
        ],
        transformRequest: [
            data => humps.decamelizeKeys(data),
            ...axios.defaults.transformRequest
        ],
        headers: {
            'x-ajax': true
        }
    })

 /*   instance.interceptors.response.use(identity, error => {
        if (error.response.status === 401) window.location.reload(true)
        return Promise.reject(error);
    });*/

    return instance
})()

export default api
