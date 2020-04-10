from django.core.exceptions import ValidationError
    
def refereeValid(val):
    
    REFEREE_RANK = [
        'Нет', 
        'Юный спортивный судья', 
        'Спортивный судья 3-й категории',
        'Спортивный судья 3-й категории',
        'Спортивный судья 3-й категории',
        'Спортивный судья всероссийской категории'
        ]

    if not val in REFEREE_RANK:
        raise ValidationError(f" '{val}' - is not a valid value for the 'referree_rank' field", code='odd', params={'value': val})


def classValid(val):
    CLASS_RANK = ['Нет','E', 'D', 'C', 'B', 'A', 'S', 'M']
    if not val in CLASS_RANK:
        raise ValidationError(f" '{val}' - is not a valid value for the 'class_rank' field", code='odd', params={'value': val})

def trainerValid(val):
    TRAINER_RANK = [
            "Нет",
            'Тренер',
            'Заслуженный тренер'
            ]
    if not val in TRAINER_RANK:
        raise ValidationError(f" '{val}' - is not a valid value for the 'trainer_rank' field", code='odd', params={'value': val})

def sportValid(val):
    SPORT_RANK = [
        'Нет',
        '3-й юношеский',
        '2-й юношеский',
        '1-й юношеский',
        "3-й взрослый",
        "2-й взрослый",
        "1-й взрослый",
        "Кандидат в мастера спорта",
        "Мастер спорта",
        "Мастер спорта международного класса",
            "Заслуженный мастер спорта"
    ]
    if not val in SPORT_RANK:
        raise ValidationError(f" '{val}' - is not a valid value for the 'sport_rank' field", code='odd', params={'value': val})
 
def genderValid(val):
    GENDER = ['м', "ж"]
    if not val in GENDER:
        raise ValidationError(f" '{val}' - is not a valid value for the 'gender' field", code='odd', params={'value': val})
 