from __future__ import division

import json
import re
import os
from datetime import date
import docx2txt
import pandas as pd
from tika import parser
import phonenumbers
import pdfplumber
import datefinder
import logging
import spacy
import sys
import operator
import string

java_path = r"C:\Users\Avi\Java\bin\java.exe"
os.environ['JAVAHOME'] = java_path

class resumeparse(object):
    objective = (
        'career goal',
        'objective',
        'career objective',
        'employment objective',
        'professional objective',
        'summary',
        'career summary',
        'professional summary',
        'summary of qualifications',
        # 'digital'
    )

    work_and_employment = (
        'employment history',
        'work history',
        'work experience',
        'relevant work experience',
        'working experience',
        'work experiences',
        'experience',
        'career history',
        'professional experience',
        'professional experiences'
        'professional background',
        'additional experience',
        'career related experience',
        'related experience',
        'programming experience',
        'freelance',
        'freelance experience',
        'army experience',
        'military experience',
        'military background',
        'business and related experience',
        'internship',
        'internship / work experience'
    )

    education_and_training = (
        'academic background',
        'academic experience',
        'academic profile',
        'academic qualifications',
        'programs',
        'qualifications',
        'courses',
        'education and professional qualifications',
        'education & professional qualifications',
        'related courses',
        'education',
        'EDUCATION',
        'educational background',
        'educational qualifications',
        'educational training',
        'education and training',
        'training',
        'academic training',
        'professional training',
        'course project experience',
        'related course projects',
        'internship experience',
        'internships',
        'apprenticeships',
        'college activities',
        'special training',
    )

    skills_header = (
        'credentials',
        'areas of experience',
        'areas of expertise',
        'areas of knowledge',
        'skills',
        'soft skills',
        "other skills",
        "other abilities",
        'career related skills',
        'professional skills',
        'specialized skills',
        'technical skills',
        'computer skills',
        'personal skills',
        'computer knowledge',
        'technical experience',
        'proficiencies',
        'programming languages',
        'competencies'
    )
    
    languages = (
        'languages',
        'language competencies and skills'
    )
    
    projects = (
        'projects',
        'personal projects',
        'academic projects'
    )
    
    certificates = (
        'certifications',
        'certificates',
        'certification',
        'professional certifications'
    )
    
    misc = (
        'activities and honors',
        'activities',
        'affiliations',
        'professional affiliations',
        'associations',
        'professional associations',
        'memberships',
        'professional memberships',
        'athletic involvement',
        'community involvement',
        'refere',
        'civic activities',
        'extra-curricular activities',
        'co-curricular activities'
        'professional activities',
        'volunteer work',
        'volunteer experience',
        'additional information',
        'interests',
        'hobbies',
        'additional info'
    )

    accomplishments = (
        'achievement',
        'licenses',
        'presentations',
        'conference presentations',
        'conventions',
        'dissertations',
        'exhibits',
        'papers',
        'publications',
        'professional publications',
        'research',
        'research grants',
        'current research interests',
        'thesis'
    )

    hobbies = (
        'hobbies',
        'hobby',
        'interests'
    )

    other_univ = (
        'college',
        'institute',
        'school',
        'university',
        'iit'
    )

def convert_docx_to_txt(docx_file):
    """
        A utility function to convert a Microsoft docx files to raw text.
        This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
        :param docx_file: docx file with gets uploaded by the user
        :type docx_file: InMemoryUploadedFile
        :return: The text contents of the docx file
        :rtype: str
    """
    try:
        text = parser.from_file(docx_file, service='text')['content']
    except RuntimeError as e:
        logging.error('Error in tika installation:: ' + str(e))
        logging.error('--------------------------')
        logging.error('Install java for better result ')
        text = docx2txt.process(docx_file)
    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "
    try:
        clean_text = re.sub(r'\n+', '\n', text)
        clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
        resume_lines = clean_text.splitlines()  # Split text blob into individual lines
        resume_lines = [re.sub('\s+|\[bookmark: _GoBack]|\[image: ]|\[image: image1.jpg]|\[image: image1.png]\[Page]', ' ', line.strip()) for line in resume_lines if
                        line.strip()]  # Remove empty strings and whitespaces
        return resume_lines, text
    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "


def convert_pdf_to_txt(pdf_file):
    """
    A utility function to convert a machine-readable PDF to raw text.
    This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
    :param input_pdf_path: Path to the .pdf file which should be converted
    :type input_pdf_path: str
    :return: The text contents of the pdf
    :rtype: str
    """
    # try:
    # PDFMiner boilerplate
    # pdf = pdfplumber.open(pdf_file)
    # full_string= ""
    # for page in pdf.pages:
    #   full_string += page.extract_text() + "\n"
    # pdf.close()

    try:
        raw_text = parser.from_file(pdf_file, service='text')['content']
    except RuntimeError as e:
        logging.error('Error in tika installation:: ' + str(e))
        logging.error('--------------------------')
        logging.error('Install java for better result ')
        pdf = pdfplumber.open(pdf_file)
        raw_text = ""
        for page in pdf.pages:
            raw_text += page.extract_text() + "\n"
        pdf.close()
    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "
    try:
        full_string = re.sub(r'\n+', '\n', raw_text)
        full_string = full_string.replace("\r", "\n")
        full_string = full_string.replace("\t", " ")

        # Remove awkward LaTeX bullet characters

        full_string = re.sub(r"\uf0b7", " ", full_string)
        full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
        full_string = re.sub(r'• ', " ", full_string)

        # Split text blob into individual lines
        resume_lines = full_string.splitlines(True)

        # Remove empty strings and whitespaces
        resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
        return resume_lines, raw_text

    except Exception as e:
        logging.error('Error in docx file:: ' + str(e))
        return [], " "

def file_to_txt(file):
    file = os.path.join(file)
    if file.endswith('docx') or file.endswith('doc'):
        resume_lines, raw_text = convert_docx_to_txt(file)
    elif file.endswith('pdf'):
        resume_lines, raw_text = convert_pdf_to_txt(file)

    elif file.endswith('txt'):

        with open(file, 'r', encoding='latin') as f:
            resume_lines = f.readlines()

    else:
        resume_lines = None
    resume_segments = segment(resume_lines)

    return resume_lines, resume_segments

def find_segment_indices(string_to_search, resume_segments, resume_indices):
    for i, line in enumerate(string_to_search):

        if line[0].islower():
            continue

        header = line.lower()

        if [o for o in resumeparse.objective if header.startswith(o)]:
            try:
                resume_segments['objective'][header]
            except:
                resume_indices.append(i)
                header = [o for o in resumeparse.objective if header.startswith(o)][0]
                resume_segments['objective'][header] = i
        elif [w for w in resumeparse.work_and_employment if header.startswith(w)]:
            try:
                resume_segments['work_and_employment'][header]
            except:
                resume_indices.append(i)
                header = [w for w in resumeparse.work_and_employment if header.startswith(w)][0]
                resume_segments['work_and_employment'][header] = i
        elif [e for e in resumeparse.education_and_training if header.startswith(e)]:
            try:
                resume_segments['education_and_training'][header]
            except:
                resume_indices.append(i)
                header = [e for e in resumeparse.education_and_training if header.startswith(e)][0]
                resume_segments['education_and_training'][header] = i
        elif [p for p in resumeparse.projects if header.startswith(p)]:
            try:
                resume_segments['projects'][header]
            except:
                resume_indices.append(i)
                header = [p for p in resumeparse.projects if header.startswith(p)][0]
                resume_segments['projects'][header] = i
        elif [s for s in resumeparse.skills_header if header.startswith(s)]:
            try:
                resume_segments['skills'][header]
            except:
                resume_indices.append(i)
                header = [s for s in resumeparse.skills_header if header.startswith(s)][0]
                resume_segments['skills'][header] = i
        elif [l for l in resumeparse.languages if header.startswith(l)]:
            try:
                resume_segments['languages'][header]
            except:
                resume_indices.append(i)
                header = [l for l in resumeparse.languages if header.startswith(l)][0]
                resume_segments['languages'][header] = i
        elif [m for m in resumeparse.misc if header.startswith(m)]:
            try:
                resume_segments['misc'][header]
            except:
                resume_indices.append(i)
                header = [m for m in resumeparse.misc if header.startswith(m)][0]
                resume_segments['misc'][header] = i
        elif [a for a in resumeparse.accomplishments if header.startswith(a)]:
            try:
                resume_segments['accomplishments'][header]
            except:
                resume_indices.append(i)
                header = [a for a in resumeparse.accomplishments if header.startswith(a)][0]
                resume_segments['accomplishments'][header] = i
        elif [c for c in resumeparse.certificates if header.startswith(c)]:
            try:
                resume_segments['certificates'][header]
            except:
                resume_indices.append(i)
                header = [c for c in resumeparse.certificates if header.startswith(c)][0]
                resume_segments['certificates'][header] = i
        elif [h for h in resumeparse.hobbies if header.startswith(h)]:
            try:
                resume_segments['hobbies'][header]
            except:
                resume_indices.append(i)
                header = [h for h in resumeparse.hobbies if header.startswith(h)][0]
                resume_segments['hobbies'][header] = i


def slice_segments(string_to_search, resume_segments, resume_indices):
    resume_segments['contact_info'] = string_to_search[:resume_indices[0]]

    for section, value in resume_segments.items():
        if section == 'contact_info':
            continue

        for sub_section, start_idx in value.items():
            end_idx = len(string_to_search)
            if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                end_idx = resume_indices[resume_indices.index(start_idx) + 1]

            resume_segments[section][sub_section] = string_to_search[start_idx:end_idx]
            #print('thsi is slice segment', resume_segments)


def segment(string_to_search):
    resume_segments = {
        'objective': {},
        'work_and_employment': {},
        'education_and_training': {},
        'projects':{},
        'skills': {},
        'languages': {},
        'accomplishments': {},
        'certificates': {},
        'hobbies': {},
        'misc': {}
    }

    resume_indices = []

    find_segment_indices(string_to_search, resume_segments, resume_indices)
    if len(resume_indices) != 0:
        slice_segments(string_to_search, resume_segments, resume_indices)
    else:
        resume_segments['contact_info'] = []
    #print('this is segment', resume_segments)
    return resume_segments

def calculate_experience(resume_text):
    #
    # def get_month_index(month):
    #   month_dict = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    #   return month_dict[month.lower()]

    def correct_year(result):
        if len(result) < 2:
            if int(result) > int(str(date.today().year)[-2:]):
                result = str(int(str(date.today().year)[:-2]) - 1) + result
            else:
                result = str(date.today().year)[:-2] + result
        return result

    # try:
    experience = 0
    start_month = -1
    start_year = -1
    end_month = -1
    end_year = -1
    exp_range = []
    not_alpha_numeric = r'[^a-zA-Z\d]'
    number = r'(\d{2})'

    months_num = r'(01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)'
    months_short = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
    months_long = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(' \
                  r'november)|(december) '
    month = r'(' + months_num + r'|' + months_short + r'|' + months_long + r')'
    regex_year = r'((20|19)(\d{2})|(\d{2}))'
    year = regex_year
    start_date = month + not_alpha_numeric + r"?" + year

    end_date = r'((' + number + r'?' + not_alpha_numeric + r"?" + month + not_alpha_numeric + r"?" + year + r')|(present|current)) '
    longer_year = r"((20|19)(\d{2}))"
    year_range = longer_year + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))" + r'(' + longer_year + r'|(present' \
                                                                                                      r'|current)) '
    date_range = r"(" + start_date + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))" + end_date + r")|(" + year_range + r")"

    regular_expression = re.compile(date_range, re.IGNORECASE)
    punc = '''!()[]{};'"\,<>?@#$%^&*_~'''
    for ele in resume_text:  
        if ele in punc:  
            resume_text = resume_text.replace(ele, " ")  
    regex_result = re.search(regular_expression, resume_text)
    try:
        exp_range.append(regex_result.group())
    except:
        pass
    while regex_result:

        date_range = regex_result.group()
        try:
            year_range_find = re.compile(year_range, re.IGNORECASE)
            year_range_find = re.search(year_range_find, date_range)
            replace = re.compile(r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))", re.IGNORECASE)
            replace = re.search(replace, year_range_find.group().strip())

            start_year_result, end_year_result = year_range_find.group().strip().split(replace.group())
            start_year_result = int(correct_year(start_year_result))
            if end_year_result.lower().find('present') != -1 or end_year_result.lower().find('current') != -1:
                end_month = date.today().month  # current month
                end_year_result = date.today().year  # current year
            else:
                end_year_result = int(correct_year(end_year_result))


        except:

            start_date_find = re.compile(start_date, re.IGNORECASE)
            start_date_find = re.search(start_date_find, date_range)

            non_alpha = re.compile(not_alpha_numeric, re.IGNORECASE)
            non_alpha_find = re.search(non_alpha, start_date_find.group().strip())

            replace = re.compile(start_date + r"(" + not_alpha_numeric + r"{1,4}|(\s*to\s*))", re.IGNORECASE)
            replace = re.search(replace, date_range)
            date_range = date_range[replace.end():]

            start_year_result = start_date_find.group().strip().split(non_alpha_find.group())[-1]

            # if len(start_year_result)<2:
            #   if int(start_year_result) > int(str(date.today().year)[-2:]):
            #     start_year_result = str(int(str(date.today().year)[:-2]) - 1 )+start_year_result
            #   else:
            #     start_year_result = str(date.today().year)[:-2]+start_year_result
            # start_year_result = int(start_year_result)
            start_year_result = int(correct_year(start_year_result))

            if date_range.lower().find('present') != -1 or date_range.lower().find('current') != -1:
                end_month = date.today().month  # current month
                end_year_result = date.today().year  # current year
            else:
                end_date_find = re.compile(end_date, re.IGNORECASE)
                end_date_find = re.search(end_date_find, date_range)

                end_year_result = end_date_find.group().strip().split(non_alpha_find.group())[-1]

                # if len(end_year_result)<2:
                #   if int(end_year_result) > int(str(date.today().year)[-2:]):
                #     end_year_result = str(int(str(date.today().year)[:-2]) - 1 )+end_year_result
                #   else:
                #     end_year_result = str(date.today().year)[:-2]+end_year_result
                # end_year_result = int(end_year_result)
                end_year_result = int(correct_year(end_year_result))

        if (start_year == -1) or (start_year_result <= start_year):
            start_year = start_year_result
        if (end_year == -1) or (end_year_result >= end_year):
            end_year = end_year_result

        resume_text = resume_text[regex_result.end():].strip()
        regex_result = re.search(regular_expression, resume_text)
        try:
            exp_range.append(regex_result.group())
        except:
            pass
    return end_year - start_year, exp_range

def get_experience(resume_segments, label = 'work'):
    total_exp = 0
    if len(resume_segments['work_and_employment'].keys()) and label == 'work':
        text = ""
        for key, values in resume_segments['work_and_employment'].items():
            text += " ".join(values) + " "
        total_exp, exp_range = calculate_experience(text)
        return total_exp, exp_range
    if len(resume_segments['education_and_training'].keys()) and label == 'education':
        text = ""
        for key, values in resume_segments['education_and_training'].items():
            text += " ".join(values) + " "
        total_exp, exp_range = calculate_experience(text)
        return total_exp, exp_range
    else:
        text = ""
        for key in resume_segments.keys():
            if key != 'education_and_training':
                if key == 'contact_info':
                    text += " ".join(resume_segments[key]) + " "
                else:
                    for key_inner, value in resume_segments[key].items():
                        text += " ".join(value) + " "
        total_exp, exp_range = calculate_experience(text)
        return total_exp, exp_range
    return total_exp, exp_range


def find_phone(text):
    try:
        return list(iter(phonenumbers.PhoneNumberMatcher(text, None)))[0].raw_string
    except:
        try:
            return re.search(
                r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',
                text).group()
        except:
            return ""


def extract_email(text):
    email = re.findall(r'\S+@\S+', text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_github(text):
    github = re.findall('github.com\S+', text)
    if github:
        try:
            return github[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_facebook(text):
    facebook = re.findall('facebook.com\S+', text)
    if facebook:
        try:
            return facebook[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_twitter(text):
    twitter = re.findall('twitter.com\S+', text)   
    if twitter:
        try:
            return twitter[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_skype(text):
    skype = re.findall('join.skype.com\S+', text)   
    if skype:
        try:
            return skype[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_linkedin(text):
    linkedin = re.findall('linkedin.com/in\S+', text)
    if linkedin:
        try:
            return linkedin[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_location(text, file):
    df = pd.read_csv(file, header=None)
    cities = [i.lower() for i in df[1]]
    location =[]
    for i in range(len(cities)):

        if re.findall(r'\b'+cities[i]+r'\b', text.lower()):
            location.append(df[1][i]+', '+df[4][i])
            break
    return location

def extract_dob(text):
    #dob = re.findall("[0-9][0-9]-[0-9][0-9]-[1-2][0-9][0-9][0-9]|[0-9][0-9]/[0-9][0-9]/[1-2][0-9][0-9][0-9]", txt)
    dob = datefinder.find_dates(text, strict= False)
    if dob:
        for match in dob:
            return match
    return None

def ner_model(text, path):
    model = spacy.load(path)
    doc = model(text)
    return doc

# re.sub(' +', ' ', listsearch[ii])):
def extract_university(text, file):
    df = pd.read_csv(file, header=None)
    universities = [i.lower() for i in df[1]]
    college_name = []
    listex = universities
    listsearch = [t.lower() for t in text]
    # listsearch = listsearch1[0].split(' ')
    for i in range(len(listex)):
        for ii in range(1,len(listsearch)):
            if re.findall(listex[i], listsearch[ii]):
                college_name.append(listex[i])
    if college_name==[]:
        for i in range(len(listsearch)):
            for keyword in resumeparse.other_univ:
                if re.findall(keyword, listsearch[i]):
                    college_name.append(listsearch[i])
                    break
    return college_name

def extract_passing_year(text_lines):
    listsearch = [t.lower() for t in text_lines]
    passing_year = []
    year = '(^19\d{2}|\s19\d{2}|^20\d{2}|\s20\d{2}|^\d{2}|\s\d{2}\s)'
    for i in range(len(listsearch)):
        if re.findall(year, listsearch[i]):
            if re.findall('present', listsearch[i]):
                passing_year.append(str(re.findall(year, listsearch[i])[0]) + 
                                    ' - Present')
            elif len(re.findall(year, listsearch[i]))>1:
                passing_year.append(str(re.findall(year, listsearch[i])[0]) 
                                     + ' - ' +
                                    str(re.findall(year, listsearch[i])[1]))
            else:
                passing_year.append(re.findall(year, listsearch[i])[0])
    return passing_year

def extract_specialization(text_lines, file):
    df = pd.read_csv(file, header = None)
    major_list = [i.lower() for i in df[1]]
    major = []
    for i in range(len(text_lines)):
        for j in range(len(major_list)):
            if re.findall(major_list[j], text_lines[i].lower()):
                major.append(major_list[j])
    return major
                
def extract_degree(text_lines, file):
    df = pd.read_csv(file, header=None)
    degree_list = [i for i in df[0]]
    deg=[]
    for i in range(len(text_lines)):
        for j in range(len(degree_list)):
            if re.findall(degree_list[j], text_lines[i]):
                deg.append(text_lines[i])
    #degree=(list(set(degree)))
    degree=[]
    for d in deg:
        if d not in degree:
            degree.append(d)
    return degree

def extract_languages(text, path):
    df = pd.read_csv(path, header=None)
    language_list = list(df[1])
    languages = []
    for i in range(len(language_list)):
        for ii in range(len(text)):
            if re.findall(language_list[i].lower(), text[ii].lower()):
                languages.append(language_list[i])
                break
    return languages

def extract_skills(text_lines, file):
    df = pd.read_csv(file, header = None)
    skill_list = [str(i).upper() for i in list(df[2].unique())]
    skill_list = list(set(skill_list))
    #print(len(skill_list))
    skills = []
    for i in range(len(text_lines)):
        for j in range(len(skill_list)):
            if re.search(re.escape(str(skill_list[j]).lower()), text_lines[i].lower()):
                skills.append(skill_list[j])
    return list(set(skills))