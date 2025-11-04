import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import cookieParser from 'cookie-parser';
import { WinstonModule } from 'nest-winston';
import { winstonConfig } from './common/logger/winston.config';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: WinstonModule.createLogger(winstonConfig),
  });

  app.use(helmet());
  app.use(cookieParser());

  app.use(
    rateLimit({
      windowMs: 15 * 60 * 1000,
      max: 100,
      standardHeaders: true,
      legacyHeaders: false,
      message: { statusCode: 429, error: 'Too many requests', retryAfter: 900 },
    }),
  );

  const authLimiter = rateLimit({
    windowMs: 10 * 60 * 1000,
    max: 5,
    skipSuccessfulRequests: true,
  });
  app.use(['/auth/login', '/auth/register'], authLimiter);

  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));

  const config = new DocumentBuilder()                 // <-- YENİ
    .setTitle('Movie Reco API')
    .setDescription('PostgreSQL + JWT + TypeORM sample')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, document)

  await app.listen(process.env.PORT ?? 3000);
  console.log(`🚀  http://localhost:${process.env.PORT ?? 3000}/docs`);
}
bootstrap();
