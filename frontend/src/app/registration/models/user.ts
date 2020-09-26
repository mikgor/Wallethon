export class User {
  id: string;
  username: string;
  token: string;
  tokenExpiration: Date;

  constructor(id, username, token, tokenExpiration) {
    this.id = id;
    this.username = username;
    this.token = token;
    this.tokenExpiration = tokenExpiration;
  }
}
