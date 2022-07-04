from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}.")

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"Не реализован метод подсчета калорий в классе "
            f"{self.__class__.__name__}")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_SPEED_MULTIPLIER: int = 18
    CALORIES_SPEED_DEGREES: int = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_SPEED_MULTIPLIER
                * self.get_mean_speed() - self.CALORIES_SPEED_DEGREES)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_h * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
                + ((self.get_mean_speed() ** 2) // self.height_sm)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight_kg)
                * (self.duration_h * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool_m * self.count_pool
            / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_name: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    right_keys_for_training: str = (
        ', '.join('{}'.format(key) for key in training_name.keys()))

    if workout_type not in training_name:
        raise ValueError(
            f"Отсутствует такой тип тренировки как "
            f"{workout_type}. Для корректной работы выберите другой вид "
            f"тренировки: {right_keys_for_training}")

    return training_name[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
