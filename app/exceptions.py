from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с указанным email адресом уже существует!'
)

PasswordMismatchException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пароли не совпадают!'
)

InvalidURLTokenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Ссылка для подтверждения недействительна или срок ее действия истек!'
)

EmailOrPasswordIsIncorrect = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Электронная почта или пароль неправильны!'
)

TokenDoesNotExist = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не существует!'
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Некорректный токен!'
)

TokenTimeHasExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Время токена истекло!'
)

NoRoomsAvailableException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Нет свободных комнат!'
)

InvalidImageFileException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Файл должен быть изображением!'
)

PageNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Страница не найдена!'
)

AccessIsDeniedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Доступ запрещен!'
)

NotFoundHotelException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Отель не существует!'
)

NotFoundRoomException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Комната не существует!'
)

NotFoundBookingException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Бронирование не существует!'
)

ErrorInBookingDateException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Ошибка в датах бронирования!'
)