from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def __create_user(self, email: str, password: str, **extra_fields) -> object:
        if not email:
            raise ValueError('User must have an email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.created_by = None
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> object:
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_superuser') is not False:
            raise ValueError('SUser must have is_superuser=False.')

        return self.__create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> object:
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.__create_user(email, password, **extra_fields)
