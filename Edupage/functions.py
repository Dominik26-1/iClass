import re

from django.db.models import Q
from edupage_api.substitution import Action, TimetableChange

from App.logger import logger
from Substitution.models import Substitution
from Timetable.models import Timetable
from Utils.python.utils import get_numeric_class


def parse_edupage_object(timetable_change: TimetableChange, orig_lesson: int, date):
    # skonvertuj triedu zo zaznamov z edupage z rimskych na arabske cisla
    student_class = get_numeric_class(timetable_change.change_class)

    # ak povodna hodina sa presunula alebo nahradila inou
    if timetable_change.action == Action.CHANGE:
        regex_match = re.search(
            r'^(?:(?P<student_group>[a-žA-Ž0-9\s\.]+):{1})?(?:\s*\({1}(?P<old_subject>[a-žA-Ž\s]+)\){1}\s*➔{1}\s*)?\s*(?P<new_subject>[a-žA-Ž\s]+)\s+\-{1}\s*(Suplovanie{1}):{1}\s*\({1}(?P<old_teacher>[A-Ža-ž\s]+)[\s)]+➔{1}\s*(?P<new_teacher>[[A-Ža-ž\s]+)',
            timetable_change.title)
        new_lesson_reg = re.search(r'za{1}[^a-žA-Ž0-9]*(?P<moved_lesson>[0-9]{1})\.?.*hod{1}\.?',
                                   timetable_change.title)
        change_room_reg = re.search(
            r'\s*Zameniť učebňu{1}:{1}\s*\({1}(?P<old_room>[a-žA-Ž0-9]+)\){1}\s*➔{1}\s*(?P<new_room>[a-žA-Ž0-9]+)',
            timetable_change.title)
        moved_lesson, old_room, new_room = None, None, None

        if regex_match:
            students_group = regex_match.group("student_group")
            old_subject, new_subject = regex_match.group("old_subject"), regex_match.group("new_subject")
            old_teacher, new_teacher = regex_match.group("old_teacher"), regex_match.group("new_teacher")

            # ak sa presunula hodina do inej ucebne
            if change_room_reg:
                old_room = change_room_reg.group("old_room")
                new_room = change_room_reg.group("new_room")

            # ak povodna hodina odpadla a bola nahradena inou novou hodinou
            # 5. hodina - TV -> nabozenstvo -> za 7.hodinu
            # new_lesson_reg = 7
            if new_lesson_reg:
                moved_lesson = new_lesson_reg.group("moved_lesson")

                # najdi novu hodinu, ktora nahradila odpadnutu
                moved_reg_les = Timetable.objects.filter(Q(lesson=moved_lesson) & Q(day=date.strftime("%A")) &
                                                         Q(student_class=student_class) & Q(valid_from__lte=date) &
                                                         (Q(valid_to__gte=date) | Q(valid_to__isnull=True)))
                # ak bola nova hodina v tom case pre danu triedu spolu s inymi hodinami
                # najdi podla skupiny, o ktoru novu hodinu sa jedna
                if len(moved_reg_les) > 1:
                    try:
                        moved_reg_les = moved_reg_les.get(student_group=students_group)
                    except Timetable.DoesNotExist:
                        logger.warning(
                            f'Nenasla sa hodina pre skupinu {students_group} z moznych hodin {[les for les in moved_reg_les]}')
                        return []
                # ak bola nova hodina jedinou hodinou pre celu triedu
                elif len(moved_reg_les) == 1:
                    moved_reg_les = moved_reg_les[0]
                else:
                    logger.warning(
                        f'Nenasla sa nova hodina s parametrami hod:{moved_lesson},{date.strftime("%A")} pre {student_class} '
                        f'z rozvrhu, ktora mala byt presunuta za hodinu v {date}, hod:{orig_lesson} pre {student_class}')
                    return []
                presunuta_hodina = Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                                timetable=moved_reg_les,
                                                new_subject=None, new_teacher=new_teacher)
                # povodna hodina, ktora odpadla alebo sa suplovala
                try:
                    orig_record = Timetable.objects.get(Q(lesson=orig_lesson) & Q(day=date.strftime("%A")) &
                                                        Q(student_class=student_class) & Q(
                        student_group=students_group) & Q(valid_from__lte=date) &
                                                        (Q(valid_to__gte=date) | Q(valid_to__isnull=True)))
                except Timetable.DoesNotExist:
                    logger.warning(
                        f'Nenasla sa povodna hodina s parametrami hod:{orig_lesson},{date.strftime("%A")} pre {student_class} a {students_group}'
                        f'z rozvrhu, ktora mala byt suplovana dna {date}')
                    return []
                odpadnuta_hodina = Substitution(date=date, new_class=None, new_lesson=None, timetable=orig_record,
                                                new_subject=None, new_teacher=None)
                return [presunuta_hodina, odpadnuta_hodina]
            # ak nie je presun za ziadnu hodinu
            # iba sa zmenila dana hodina v dany cas na inu hodinu bez presunu
            else:
                try:

                    orig_record = Timetable.objects.get(Q(lesson=orig_lesson) & Q(day=date.strftime("%A")) &
                                                        Q(student_class=student_class) & Q(
                        student_group=students_group) & Q(valid_from__lte=date) &
                                                        (Q(valid_to__gte=date) | Q(valid_to__isnull=True)))
                except Timetable.DoesNotExist:
                    logger.warning(
                        f'Nenasla sa povodna hodina s parametrami hod:{orig_lesson},{date.strftime("%A")} pre {student_class} a {students_group}'
                        f'z rozvrhu, ktora mala byt suplovana dna {date}')
                    return []

                return [Substitution(date=date, new_class=new_room, new_lesson=orig_lesson,
                                     timetable=orig_record,
                                     new_subject=new_subject, new_teacher=new_teacher)]
    # ak odpadla povodna hodina
    elif timetable_change.action == Action.DELETION:

        regex_match = re.search(
            r'(?:(?P<student_group>[a-žA-Ž0-9\.\s]+):{1})?\s*(?P<subject>[a-žA-Ž\s]+)\s*\-{1}\s*(?P<teacher>[a-žA-Ž\s]+)',
            timetable_change.title)
        if regex_match:
            students_group = regex_match.group("student_group")
            subject = regex_match.group("subject")
            teacher = regex_match.group("teacher")

            try:

                orig_record = Timetable.objects.get(Q(lesson=orig_lesson) & Q(day=date.strftime("%A")) &
                                                    Q(student_class=student_class) & Q(
                    student_group=students_group) & Q(valid_from__lte=date) &
                                                    (Q(valid_to__gte=date) | Q(valid_to__isnull=True)))
            except Timetable.DoesNotExist:
                logger.warning(
                    f'Nenasla sa povodna hodina s parametrami hod:{orig_lesson},{date.strftime("%A")} pre triedu:{student_class} a skupinu:{students_group} '
                    f'z rozvrhu, ktora mala odpadnut dna {date}')
                return []

            return [Substitution(date=date, new_class=None, new_lesson=None,
                                 timetable=orig_record,
                                 new_subject=None, new_teacher=None)]
        else:
            return []
    else:
        return []
