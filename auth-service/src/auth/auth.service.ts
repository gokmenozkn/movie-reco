import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';
import { UsersService } from 'src/users/users.service';
import { RegisterDto } from './dto/register.dto';

@Injectable()
export class AuthService {
  constructor(
    private users: UsersService,
    private jwt: JwtService
  ) {}

  async validate(email: string, plainPass: string): Promise<any> {
    const user = await this.users.findByEmail(email);
    if (user && (await bcrypt.compare(plainPass, user.password)))
      return { id: user.id, email: user.email };
    throw new UnauthorizedException('Invalid credentials');
  }

  async login(user: any) {
    const payload = { sub: user.id, email: user.email };
    return { access_token: this.jwt.sign(payload) };
  }

  async register(dto: RegisterDto) {
    const user = await this.users.create(dto.email, dto.password);
    return this.login(user);
  }
}
