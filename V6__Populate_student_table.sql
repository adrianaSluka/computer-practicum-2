INSERT INTO Student(Student_ID, BirthDate, Sex, RegTypeName, ClassProfile, ClassLang, ExamYear, Place_ID, School_ID)
SELECT DISTINCT out_id, birth, sex, reg_type, class_profile, class_lang, year,
(SELECT DISTINCT a.Place_ID
FROM (SELECT DISTINCT Place_ID, RegName, AreaName, TerName
	FROM Place
	WHERE RegName IS NOT NULL AND AreaName IS NOT NULL AND TerName IS NOT NULL) as a
WHERE RegName=region AND AreaName=area AND TerName=tername) as pid,
(SELECT DISTINCT b.School_ID
FROM (SELECT DISTINCT School_ID, Name, ParentName, Place_ID
	FROM School
	WHERE ParentName IS NOT NULL) as b
WHERE Name=EOName AND ParentName=EOParent) as school_id
FROM zno
WHERE birth IS NOT NULL
ON CONFLICT DO NOTHING;