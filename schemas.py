import os
import io
from typing import List, Optional
from dotenv import load_dotenv
import streamlit as st
from pydantic import BaseModel, Field
import docx

# ==============================================================================
# 1. Pydantic Schema Definitions
# ==============================================================================

class ContactInfo(BaseModel):
    phone: str
    linkedin: str
    email: str
    github: str

class PersonalInfo(BaseModel):
    name: str
    title: str
    contact: ContactInfo

class WorkExperienceItem(BaseModel):
    role: str
    organization: str
    period: str
    highlights: List[str]

class TechnicalProjectItem(BaseModel):
    name: str
    technologies: str
    highlights: List[str]

class EducationItem(BaseModel):
    degree: str
    institution: str
    period: str
    honors_or_notes: Optional[str] = None

class MilitaryService(BaseModel):
    role: str
    period: str
    description: str

class LanguageItem(BaseModel):
    language: str
    proficiency: str

class ProfessionalSkills(BaseModel):
    languages: List[str] = Field(default_factory=list)
    software_development: List[str] = Field(default_factory=list)
    data_analysis_and_visualization: List[str] = Field(default_factory=list)
    environments: Optional[List[str]] = Field(default_factory=list)
    bioinformatics_and_domain_tools: Optional[List[str]] = Field(default_factory=list)
    machine_learning: Optional[List[str]] = Field(default_factory=list)
    soft_skills: Optional[List[str]] = Field(default_factory=list)

class TailoredResume(BaseModel):
    personal_info: PersonalInfo
    about_me: str
    work_experience: List[WorkExperienceItem]
    technical_projects: Optional[List[TechnicalProjectItem]] = []
    professional_skills: ProfessionalSkills
    education: List[EducationItem]
    military_service: Optional[MilitaryService] = None
    languages: List[LanguageItem]