// 登录
export function login(data) {
  return request({
    url: "/api/court/login",
    method: "post",
    data,
  });
}
// 获取验证码
export function captchaImage(params) {
  return request({
    url: "/api/captchaImage",
    method: "get",
    params,
  });
}
// 获取登录用户信息
export function getInfo(params) {
  return request({
    url: "/api/court/getInfo",
    method: "get",
    params,
    headers: {
      Authorization: JSON.parse(localStorage.Authorization),
    },
  });
}
