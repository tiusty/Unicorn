/**
 * Contains the URLS for the survey app
 *
 * The format/naming should match the urls.py
 */
const app_name = '/survey';
const api_path = app_name + '/api';

const survey_endpoints = {
    'rentSurveyResult': '/survey/rent/',
    'rentingSurvey': '/survey/rent/',
    'rentSurvey': '/survey/api/rentSurvey/',
    'tenants':  api_path + '/tenants/',
};

export default survey_endpoints;