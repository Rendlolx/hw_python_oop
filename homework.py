from dataclasses import dataclass
from typing import Dict, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

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
            "Не реализован метод подсчета калорий в классе "
            + self.__class__.__name__)

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
    coeff_cal_first = 18
    coeff_cal_second = 20
    MIN_IN_H = 60

    def get_spent_calories(self) -> float:
        return ((self.coeff_cal_first
                * super().get_mean_speed() - self.coeff_cal_second)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_h * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_cal_first = 0.035
    coeff_cal_second = 0.029
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        return (self.coeff_cal_first * self.weight_kg
                + ((float(super().get_mean_speed()) ** 2) // self.height_sm)
                * self.coeff_cal_second) * (self.duration_h * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_cal_first = 1.1
    coeff_cal_second = 2
    LEN_STEP = 1.38

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
                + self.coeff_cal_first) * self.coeff_cal_second
                * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_name: Dict[str, List[int]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }

    if workout_type in training_name:
        return training_name[workout_type](*data)
    else:
        return ValueError(
            f"Отсутствует такой тип тренировки как "
            f"{workout_type}")


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
