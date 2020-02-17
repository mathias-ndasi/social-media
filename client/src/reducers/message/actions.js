export const SET_MESSAGE = 'SET_MESSAGE'
export const RESET_MESSAGE = 'RESET_MESSAGE'


export const setMessage = message => {
    return {
        type: SET_MESSAGE,
        message
    }
}

export const resetMessage = () => {
    return {
        type: RESET_MESSAGE
    }
}