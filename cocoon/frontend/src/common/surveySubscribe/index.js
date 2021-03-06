import React, { Component } from 'react';
import './surveySubscribe.css';
import PropTypes from "prop-types";
import axios from 'axios';

// Cocoon Modules
import survey_endpoints from '../../endpoints/survey_endpoints';

export default class SurveySubscribe extends Component {

    state = {
        wants_update: false,
        num_home_threshold: 0,
        score_threshold: 0
    }

    componentDidMount() {
        this.getSurveyData()
    }

    getSurveyData = () => {
        /**
         * Function retrieves the survey_subscribe information
         */
        let endpoint = survey_endpoints['rentSurvey'] + this.props.survey_id;
        axios.get(endpoint,
            {
                params: {
                    data_type: 'survey_subscribe',
                }
            })
            .catch(error => console.log('BAD', error))
            .then(response => {
                this.setState({
                    num_home_threshold: response.data.num_home_threshold,
                    wants_update: response.data.wants_update,
                    score_threshold: response.data.score_threshold,
                })
            })
    }

    updateSurveyData = () => {
        /**
         * Function updates the survey with the new survey subscribe information
         */
        let endpoint = survey_endpoints['rentSurvey'] + this.props.survey_id +'/';
        axios.put(endpoint,
            {
                type: 'survey_subscribe',
                data: {
                    'num_home_threshold': this.state.num_home_threshold,
                    'wants_update': this.state.wants_update,
                    'score_threshold': this.state.score_threshold,
                },
            })
            .catch(error => console.log('BAD', error))
            .then(response => {
                this.setState({
                    num_home_threshold: response.data.num_home_threshold,
                    wants_update: response.data.wants_update,
                    score_threshold: response.data.score_threshold,
                })
            })
    }

    subscribe = () => {
        if (this.state.wants_update) {
            // subscribes to survey by this.props.survey_id
            console.log('subscribed!');
        } else {
            console.log('unsub?')
        }
    }

    toggleSubscribe = () => {
        this.setState({
            wants_update: !this.state.wants_update
        }, () => {
            this.updateSurveyData();
        })
    }

    renderCheckbox = () => {
        let checkbox = 'check_box_outline_blank';
        if (this.state.wants_update) {
            checkbox = 'check_box';
        }
        return checkbox;
    }

    saveValue = (e) => {
        const { name, value } = e.target;
        let field_value = 0;
        if (name === 'score_threshold') {
            if (value < 0) {
                field_value = 0
            } else if (value > 100) {
                field_value = 100
            } else {
                field_value = value
            }
        } else if (name === 'num_home_threshold') {
            if (value < 0) {
                field_value = 0
            } else if (value > 200) {
                field_value = 200
            } else {
                field_value = value
            }
        } else {
            field_value = value
        }

        this.setState({
            [name]: field_value
        })
    }

    renderOptions = () => {
        if (this.state.wants_update) {
            return (
                <div className="subscribe-options">
                    Send me an email when
                    <input type="number" value={this.state.num_home_threshold} name="num_home_threshold" onChange={this.saveValue} onBlur={this.updateSurveyData} />
                    {this.state.num_home_threshold === 1 ? 'home has' : 'homes have'} a score of at least
                    <input type="number" value={this.state.score_threshold} name="score_threshold" onChange={this.saveValue} onBlur={this.updateSurveyData} />
                </div>
            );
        }
    }

    render() {
        return (
            <div className="subscribe-wrapper">
                    <div className="subscribe-checkbox" onClick={this.toggleSubscribe}>
                        <i className="material-icons">{this.renderCheckbox()}</i>
                        Set up notifications to keep me updated on new postings I'll love.
                    </div>
                    {this.renderOptions()}
                </div>
        );
    }
}

SurveySubscribe.propTypes = {
    survey_id: PropTypes.number.isRequired
}