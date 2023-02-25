
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('prima', '1. poschodie', false, false, false, false, true, false, false);
INSERT INTO public."Classrooms"
("name", "position", "interactive_board", "teacher_pc", "teacher_notebook", "flip_chart", "sink", "data_projector", "ethernet_cable")
VALUES('ucuj2', '3. poschodie', true, false, true, true, false, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('uinf2', '3. poschodie', true, false, true, true, false, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('uinf3', '3. poschodie', true, true, true, true, false, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('tev1', 'prizemie', false, false, false, false, true, false, false);

INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('tev2', 'podzemie', false, false, false, false, true, false, false);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('unab', '2.poschodie', false, false, false, true, true, true, false);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('sekunda', '1.poschodie', true, false, false, true, true, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('tercia', '2.poschodie', true, false, false, false, true, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('lchem', 'prizemie', false, false, false, false, true, false, false);

INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('lfyz', 'prizemie', false, false, false, false, true, false, false);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('kvarta', '2.pochodie', false, true, false, false, true, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('kvinta', '1.pochodie', true, true, false, false, false, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('ufyz', 'prizemie', false, false, false, false, false, true, true);
INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('ubio', 'prizemie', false, false, false, true, true, true, false);

INSERT INTO public."Classrooms"
("name", "position", interactive_board, teacher_pc, teacher_notebook, flip_chart, sink, data_projector, ethernet_cable)
VALUES('uanj1', '1.pochodie', true, true, false, true, true, true, true);


INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Monday',1, 'ANJ', 'Michalov', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Monday',2, 'GEO', 'Hornanska', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Monday',3, 'MAT', 'Trenklerova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Monday',4, 'SJL', 'Candova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Monday',5, 'INF', 'Fricova', 3);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Tuesday',1, 'VYV', 'Cepelova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Tuesday',2, 'MAT', 'Trenklerova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Tuesday',3, 'SJL', 'Candova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Tuesday',4, 'KNB', 'Sr. Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Tuesday',5, 'DEJ', 'Zalomova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Wednesday',1, 'ANJ', 'Marcincinova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Wednesday',2, 'SJL', 'Candova' 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Wednesday',3, 'MAT', 'Trenklerova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Wednesday',4, 'NEJ', 'Husekova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Wednesday',5, 'OBN', 'Cizmarova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Thursday',1, 'MAT', 'Trenklerova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Thursday',2, 'ANJ', 'Michalov', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Thursday',3, 'SJL', 'Candova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Thursday',4, 'NEJ', 'Husekova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Thursday',5, 'BIO', 'Jascurova', 15);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Friday',1, 'SJL', 'Candova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Friday',2,  'MAT', 'Trenklerova', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Friday',3, 'TSV', 'Svik', 5);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Friday',4, 'ANJ', 'Michalov', 1);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('prima', 'Friday',5, 'KNB', 'Sr.Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Monday',1, 'NEJ', 'Antesova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Monday',2, 'SJL', 'Korfantova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Monday',3, 'CHE', 'Tutokyova', 10);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Monday',4, 'FYZ', 'Svikova', 11);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Monday',5, 'MAT', 'Trenklerova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Tuesday',1, 'ANJ', 'Marcincinova', 16);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Tuesday',2, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Tuesday',3, 'OBN', 'Cizmarova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Tuesday',4, 'MAT', 'Trenklerova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Tuesday',5, 'TSV', 'Svik', 6);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Wednesday',1, 'MAT', 'Trenklerova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Wednesday',2, 'GEO', 'Hornanska' 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Wednesday',3, 'SJL', 'Korfantova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Wednesday',4, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Wednesday',5, 'ANJ', 'Marcincinova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Thursday',1, 'BIO', 'Tutokyova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Thursday',2, 'MAT', 'Trenklerova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Thursday',3, 'CHE', 'Tutokyova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Thursday',4, 'SJL', 'Korfantova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Thursday',5, 'ANJ', 'Hadobas', 16);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Friday',1, 'FYZ', 'Svikova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Friday',2, 'ANJ', 'Marcincinova', 16);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Friday',3, 'KNB', 'Sr.Karola', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Friday',4, 'SJL', 'Korfantova', 12);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvarta', 'Friday',5, 'INF', 'Fricova', 4);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Monday',1, 'GEO', 'Hornanska', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Monday',2, 'KNB', 'Sr.Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Monday',3, 'MAT', 'Macko', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Monday',4, 'RUJ', 'Pitonakova', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Monday',5, 'BIO', 'Golianova', 15);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Tuesday',1, 'FYZ', 'Svikova', 11);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Tuesday',2, 'SJL', 'Radimska', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Tuesday',3, 'MAT', 'Macko', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Tuesday',4, 'DEJ', 'Zalomova', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Tuesday',5, 'ANJ', 'Michalov', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Wednesday',1, 'SJL', 'Radimska', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Wednesday',2, 'RUJ', 'Pitonakova' 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Wednesday',3, 'MAT', 'Macko', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Wednesday',4, 'BIO', 'Golianova', 3);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Wednesday',5, 'ZRUZ', 'Sr.Adriana', 3);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Thursday',1, 'MAT', 'Macko', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Thursday',2, 'SJL', 'Radimska', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Thursday',3, 'ANJ', 'Michalov', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Thursday',4, 'INF', 'Fricova', 4);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Thursday',5, 'INF', 'Fricova', 4);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Friday',1, 'ANJ', 'Hadobas', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Friday',2, 'TSV', 'Svik', 5);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Friday',3, 'RUJ', 'Pitonakova', 13);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Friday',4, 'KNB', 'Sr.Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('kvinta', 'Friday',5, 'CHE', 'Svikova', 11);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Monday',1, 'CHE', 'Simegova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Monday',2, 'BIO', 'Tutokyova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Monday',3, 'SJL', 'Korfantova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Monday',4, 'MAT', 'Trenklerova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Monday',5, 'ANJ', 'Michalov', 16);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Tuesday',1, 'SJL', 'Korfantova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Tuesday',2, 'INF', 'Fricova', 4);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Tuesday',3, 'ANJ', 'Michalov', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Tuesday',4, 'SJL', 'Korfantova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Tuesday',5, 'TSV', 'Svik', 5);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Wednesday',1, 'SJL', 'Korfantova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Wednesday',2, 'MAT', 'Trenklerova' 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Wednesday',3, 'ANJ', 'Michalov', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Wednesday',4, 'GEO', 'Hornanska', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Wednesday',5, 'FYZ', 'Svikova', 11);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Thursday',1, 'FYZ', 'Svikova', 11);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Thursday',2, 'DEJ', 'Zalomova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Thursday',3, 'MAT', 'Trenklerova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Thursday',4, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Thursday',5, 'KNB', 'Sr.Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Friday',1, 'CHE', 'Simegova', 10);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Friday',2, 'ANJ', 'Hadobas', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Friday',3, 'SJL', 'Korfantova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Friday',4, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('tercia', 'Friday',5, 'MAT', 'Trenklerova', 9);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Monday',1, 'SJL', 'Korfantova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Monday',2, 'MAT', 'Jascurova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Monday',3, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Monday',4, 'TSV', 'Bolna', 5);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Monday',5, 'ANJ', 'Hadobas', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Tuesday',1, 'MAT', 'Jascurova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Tuesday',2, 'VYV', 'Cepelova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Tuesday',3, 'SJL', 'Korfantova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Tuesday',4, 'ANJ', 'Michalov', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Tuesday',5, 'KNB', 'Sr.Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Wednesday',1, 'CHE', 'Simegova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Wednesday',2, 'FYZ', 'Svikova' 11);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Wednesday',3, 'INF', 'Fricova', 4);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Wednesday',4, 'BIO', 'Trenklerova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Wednesday',5, 'KNB', 'Sr.Karola', 7);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Thursday',1, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Thursday',2, 'MAT', 'Jascurova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Thursday',3, 'SJL', 'Korfantova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Thursday',4, 'OBN', 'Cizmarova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Thursday',5, 'GEO', 'Hornanska', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Friday',1, 'ANJ', 'Michalov', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Friday',2, 'SJL', 'Korfantova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Friday',3, 'NEJ', 'Antesova', 2);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Friday',4, 'MAT', 'Jascurova', 8);
INSERT INTO public."Timetables"
(student_class, "day", lesson, subject, teacher, classroom_id)
VALUES('sekunda', 'Friday',5, 'TSV', 'Bolna', 6);
 

INSERT INTO public."Substitutions"
("date", timetable_id)
VALUES('20/2/2023', 1);
INSERT INTO public."Substitutions"
("date", new_teacher, new_class_id, timetable_id)
VALUES('20/2/2023', 'Macko', 12, 30);
INSERT INTO public."Substitutions"
("date", new_subject, new_teacher, new_class_id, timetable_id)
VALUES('20/2/2023', 'INF', 'Bruothova', 3, 125);