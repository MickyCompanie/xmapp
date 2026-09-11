export const formatApiError = (error) => {
    let errors = {}
    error.data?.detail?.forEach(element => {
      errors[element.loc[1]] = element.msg
    });

    return errors
}