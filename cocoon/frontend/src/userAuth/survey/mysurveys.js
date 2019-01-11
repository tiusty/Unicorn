// Import React Components
import React from 'react'
import {Component} from 'react';
import axios from 'axios'

// Import Cocoon Components
import SurveySmall from "./surveySmall/surveySmall";
import signature_endpoints from "../../endpoints/signatures_endpoints";
import scheduler_endpoints from "../../endpoints/scheduler_endpoints";
import survey_endpoints from "../../endpoints/survey_endpoints";

// Import styling
import './mysurveys.css'

export default class MySurveys extends Component {

    state = {
        // State regarding the document
        hunter_doc_manager_id: null,
        is_pre_tour_signed: false,
        refreshing_document_status: false,
        pre_tour_forms_created: false,

        survey_clicked_id: undefined,
        loading_clicked: false,
        // Stores the ids of all the surveys associated with the user
        surveys: [],
        loaded: false,

        // Itinerary information
        itinerary_exists: false,

        // Stores information regarding the state of signing documents

        // Stores the survey_endpoint needed for this Component
        survey_endpoint: survey_endpoints['rentSurvey'],
        signature_endpoint: signature_endpoints['hunterDocManager'],
    };

    parseData(data) {
        /**
         * Parses data returned from the survey_endpoint and returns it in a nicer format for react
         *
         * Expects to be passed data a list of surveys from the backend and then returns a list
         *  of the survey ids.
         * @type {Array}: A list of surveys
         */
        let survey_ids = [];

        // For each survey just push the id for that survey to the list
        data.map(c =>
            survey_ids.push({
                id: c.id,
                visit_list_length: c.visit_list.length,
                favorites_length: c.favorites.length,
                url: c.url,
                name: c.name
            })
        );

        // Return the list of ids
        return survey_ids
    }

    determineActiveItinerary(data) {
        /**
         * Determines if there is an active itinerary are not
         *  An active itinerary is one that finished is not true
         *
         *  Arguments:
         *      data: list(ItinerarySerializer)
         *
         *  return (boolean):
         *      true -> If an unfinished itinerary exists
         *      false -> If there are no unfinished itineraries
         */
        let result = false;

        // Determine if any of the itineraries are not finished
        data.map(i =>
            {
                if (!i.finished) {
                    result = true
                }
            }
        );

        return result
    }

    componentDidMount() {
        /**
         *  Retrieves all the surveys associated with the user
         */
        axios.get(this.state.survey_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({surveys: this.parseData(response.data)})
            });

        /**
         Retrieves the users HunterDocManager
         */
        axios.get(this.state.signature_endpoint)
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    hunter_doc_manager_id: response.data[0].id,
                    pre_tour_forms_created: response.data[0].pre_tour_forms_created,
                    is_pre_tour_signed: response.data[0].is_pre_tour_signed,
                })
            });

        /**
         * Updates the users pre_tour_docs and checks to see if it is signed.
         *  Since the id for the url doesn't matter, null can be passed so the
         *  update function is called
         */
        let endPoint = this.state.signature_endpoint + 'null' + '/';
        axios.put(endPoint,
            {
                type: 'pre_tour_check',
            })
            .catch(error => console.log('BAD', error))
            .then(response => {
                this.setState({
                    loaded: true,
                    is_pre_tour_signed: response.data.is_pre_tour_signed,
                    pre_tour_forms_created: response.data.pre_tour_forms_created,
                })
            });

        // Determines if an itinerary exists yet already or not
        axios.get(scheduler_endpoints['itineraryClient'])
            .catch(error => console.log('Bad', error))
            .then(response => {
                this.setState({
                    itinerary_exists: this.determineActiveItinerary(response.data),
                })
            });
    }

    createDocument = () => {
        /**
         * Sends an API request to create the document specified by the template type
         */
        this.setState({
            refreshing_document_status: true,
        });
        let endpoint = signature_endpoints['hunterDoc'];
        axios.post(endpoint,
            {
                type: 'pre_tour',
            })
            .catch(error => {
                this.setState({
                    refreshing_document_status: false,
                });
                console.log('Bad', error)
            })
            .then(response =>
                this.setState({
                    id: response.data.id,
                    is_signed: response.data.is_signed,
                    pre_tour_forms_created: true,
                    refreshing_document_status: false,
                })
            );
    };

    handleOnClickCreateDocument = () => {
        if (this.state.refreshing_document_status) {
            return false
        } else {
            this.createDocument()
        }
    }

    renderTourSummary() {
        if (!this.state.is_pre_tour_signed && !this.state.pre_tour_forms_created) {
            return(
                <div>
                    <p>You need to sign the pre tour documents before scheduling a tour</p>
                    <button className="btn btn-primary" onClick={this.handleOnClickCreateDocument}>{this.state.refreshing_document_status ? 'Loading' : 'Send'}</button>
                </div>
            );
        }
    }

    render() {
        return (
            <div className="row">
                <div className="col-md-8">
                    <div className="surveys-div">
                        <h2 className="surveys-title">My Surveys</h2>
                        <p className='surveys-title-text'>When you are ready please follow the steps on the right side of the screen to
                            sign your documents so you can schedule a tour</p>
                    </div>
                    <div className="surveys-main">
                        {this.state.surveys.map(survey =>
                            <div key={survey.id} className="survey-small">
                                <SurveySmall
                                    key={survey.id}
                                    id={survey.id}
                                    name={survey.name}
                                    url={survey.url}
                                    favorites_length={survey.favorites_length}
                                    visit_list_length={survey.visit_list_length}
                                    onLoadingClicked={this.setLoadingClick}
                                    onClickSurvey={this.handleClickSurvey}
                                />
                            </div>
                        )}
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="tour-summary">
                        <h2 className="surveys-title">Tour Summary</h2>
                        {this.renderTourSummary()}
                    </div>
                </div>
            </div>
        );
    }
}