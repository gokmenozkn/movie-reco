import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsString, Length } from 'class-validator';

export class RegisterDto {
  @IsEmail() 
  @ApiProperty({ format: 'email', example: 'alice@test.com' })
  email: string;
  
  @IsString() 
  @Length(6, 50)
  @ApiProperty({ minLength: 6, example: '123456' })
  password: string;
}