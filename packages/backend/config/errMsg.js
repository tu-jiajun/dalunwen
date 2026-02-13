// 业务错误码
module.exports = {
  DEFAULT: {
    statusCode: 500,
    code: 50001,
    message: '服务端错误',
  },
  USER_NOT_FOUND: {
    statusCode: 401,
    code: 40001,
    message: '用户名或密码错误',
  },
  UNAUTHORIZED: {
    statusCode: 401,
    code: 40002,
    message: '未登录，请先登录！',
  },
  USERNAME_ALREADY_EXISTS: {
    statusCode: 200,
    code: 20001,
    message: '用户名已被占用',
  },
  'jwt expired': {
    statusCode: 401,
    code: 40101,
    message: '登录已过期，请重新登录',
  },
  'invalid token': {
    statusCode: 401,
    code: 40102,
    message: '无效的 token，请重新登录',
  },
  'jwt malformed': {
    statusCode: 401,
    code: 40103,
    message: 'Token 格式错误，请重新登录',
  },
};
