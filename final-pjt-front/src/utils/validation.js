const isValidUsername = username => {
  const trimmed = username.trim();
  if (trimmed.length > 4 && trimmed.length < 20) return true
  return false
}

const isValidPassword = password => {
  const trimmed = password.trim();
  const reg_pwd = /^.*(?=.{8,20})(?=.*[0-9])(?=.*[a-zA-Z]).*$/;
  if(!reg_pwd.test(trimmed)) return false;
  return true
}

const isValidConfirmation = (password, confirmation) => {
  const trimmed = confirmation.trim();
  if(password.trim() !== trimmed) {
    return false
  }
  return true
}

export {
  isValidUsername,
  isValidPassword,
  isValidConfirmation,
};
