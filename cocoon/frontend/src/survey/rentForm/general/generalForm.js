import React from 'react';
import { Component } from 'react';
import axios from "axios";
import moment from 'moment';
import InputRange from 'react-input-range';
import DayPicker from 'react-day-picker';
import 'react-day-picker/lib/style.css';

import { compose, withProps } from "recompose";
import {
  withGoogleMap,
  GoogleMap,
    Polygon,
} from "react-google-maps";
import DrawingManager from "react-google-maps/lib/components/drawing/DrawingManager"

import houseDatabase_endpoints from "../../../endpoints/houseDatabase_endpoints";

import SurveyQuestionHeader from '../surveyQuestionHeader';

export default class GeneralForm extends Component {
    state = {
        home_type_options: [],
        errorMessages: {
            name_error_undefined: 'You must enter the names of the tenants.',
            name_error_format: 'Enter both the first and last name.',
            home_type_error: 'You must select at least one type of home.',
            price_error_range: 'The price must be between $0 and $4000',
            price_error_weight: 'You must choose how much you care about the price.',
            date_error: 'You must select an earliest and latest move in date.',
            num_bedrooms_error_undefined: 'You must choose the number of bedrooms you need.',
            move_weight: 'You must select how badly you need to move.'
        }
    };

    componentDidMount = () => {
        // Retrieve all the home types

        // Note as of right now we only support one home type, so we default the home type to apartment
        axios.get(houseDatabase_endpoints['home_types'])
            .then(res => {
                const home_type_options = res.data;
                this.setState({ home_type_options });
            });
    };

    handleValidation = () => {
        let valid = true;
        valid = valid && this.handleNameValidation();
        valid = valid && this.handleHomeTypeValidation();
        valid = valid && this.handlePriceValidation();
        valid = valid && this.handleUrgencyValidation();
        valid = valid && this.handleDatePickerValidation();
        valid = valid && this.handleBedroomValidation();
        return valid
    };

    handleNameValidation() {
        let valid = true;
        if (this.props.tenants.length < this.props.number_of_tenants) {
            valid = false
            document.querySelector('#name_of_tenants_error').style.display = 'block';
            document.querySelector('#name_of_tenants_error').innerText = this.state.errorMessages.name_error_undefined;
            document.querySelector('#tenant_names').scrollIntoView(true)
            alert(this.state.errorMessages.name_error_undefined)
        } else {
            for(let i=0; i<this.props.number_of_tenants; i++) {
                if(!this.props.tenants[i].first_name || !this.props.tenants[i].last_name) {
                    valid = false;
                    document.querySelector('#name_of_tenants_error').style.display = 'block';
                    document.querySelector('#name_of_tenants_error').innerText = this.state.errorMessages.name_error_format;
                    document.querySelector('#tenant_names').scrollIntoView(true)
                    alert(this.state.errorMessages.name_error_format)
                }
            }
        }
        if(valid) {
            let selection = document.querySelector('#name_of_tenants_error');
            if (selection) {
                selection.style.display = 'none';
            }
        }
        return valid
    }

    handleHomeTypeValidation() {
        let valid = true;
        if (this.props.generalInfo.home_type.length === 0) {
            document.querySelector('#home_type_error').style.display = 'block';
            document.querySelector('#home_type_error').innerText = this.state.errorMessages.home_type_error;
            document.querySelector('input[name=home_type]').parentNode.scrollIntoView(true);
            alert(this.state.errorMessages.home_type_error);
            valid = false;
        }
        if(valid) { document.querySelector('#home_type_error').style.display = 'none'; }
        return valid
    }

    handlePriceValidation() {
        let valid = true;
        if (this.props.desired_price < 0) {
            document.querySelector('#price_error').style.display = 'block';
            document.querySelector('#price_error').innerText = this.state.errorMessages.price_error_range;
            document.querySelector('.input-range').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.price_error_range)
            valid = false
        }
        if (this.props.max_price < 0) {
            document.querySelector('#price_error').style.display = 'block';
            document.querySelector('#price_error').innerText = this.state.errorMessages.price_error_range;
            document.querySelector('.input-range').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.price_error_range)
            valid = false
        }
        if (this.props.price_weight < 0) {
            document.querySelector('#price_weight_error').style.display = 'block';
            document.querySelector('#price_weight_error').innerText = this.state.errorMessages.price_error_weight;
            document.querySelector('input[name=price_weight]').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.price_error_weight)
            valid = false
        }
        if(valid) { document.querySelector('#price_weight_error').style.display = 'none'; }
        if(valid) { document.querySelector('#price_error').style.display = 'none'; }
        return valid
    }

    handleDatePickerValidation() {
        let valid = true;
        if (this.props.generalInfo.move_weight !== 3) {
            if (this.props.generalInfo.earliest_move_in === undefined ||
            this.props.generalInfo.latest_move_in === undefined) {
                document.querySelector('#date_error').style.display = 'block';
                document.querySelector('#date_error').innerText = this.state.errorMessages.date_error;
                document.querySelector('.date-wrapper').parentNode.scrollIntoView(true)
                alert(this.state.errorMessages.date_error)
                valid  = false
            } else if(valid) { document.querySelector('#date_error').style.display = 'none'; }
        }
        return valid
    }

    handleUrgencyValidation() {
        let valid = true;
        if (this.props.generalInfo.move_weight === undefined) {
            document.querySelector('#move_weight_error').style.display = 'block';
            document.querySelector('#move_weight_error').innerText = this.state.errorMessages.move_weight;
            document.querySelector('input[name=move_weight]').parentNode.scrollIntoView(true)
            alert(this.state.errorMessages.move_weight);
            valid = false
        }
        if(valid) {
            let selection = document.querySelector('#move_weight_error');
            if (selection) {
                selection.style.display = 'none';
            }
        }
        return valid
    }

    handleBedroomValidation() {
        let valid = true;
        if (this.props.generalInfo.num_bedrooms.length === 0){
            document.querySelector('#number_of_rooms_error').style.display = 'block';
            document.querySelector('#number_of_rooms_error').innerText = this.state.errorMessages.num_bedrooms_error_undefined;
            document.querySelector('input[name=num_bedrooms]').parentNode.scrollIntoView(true);
            alert(this.state.errorMessages.num_bedrooms_error_undefined);
            valid = false
        }
        if(valid) { document.querySelector('#number_of_rooms_error').style.display = 'none'; }
        return valid;
    }

    renderNumberOfPeopleQuestion() {
        return (
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <SurveyQuestionHeader
                    surveyQuestion={'How many people are you <span>searching with</span>?'}
                    hasHelp={true}
                    surveyQuestionHelpText={`Please select the number of people you want to live with.\n
                    You will not be able to change the number of people once the survey is complete but you can always take another survey at any time if the number of people you are living with change.`}
                />
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="1" checked={this.props.number_of_tenants === 1} onChange={() => {}} />
                    <div>Just Me</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="2" checked={this.props.number_of_tenants === 2} onChange={() => {}} />
                    <div>Me + 1 other</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="3" checked={this.props.number_of_tenants === 3} onChange={() => {}} />
                    <div>Me + 2 others</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="number_of_tenants" value="4" checked={this.props.number_of_tenants === 4} onChange={() => {}} />
                    <div>Me + 3 others</div>
                </label>
            </div>
        );
    }

    setNameOnField(id, field_name) {
        // Display the name if the tenant exists and either a first or last name exists
        if(this.props.tenants.length > id) {
            if(field_name === 'first' && this.props.tenants[id].first_name) {
                return this.props.tenants[id].first_name;
            }

            if(field_name === 'last' && this.props.tenants[id].last_name) {
                return this.props.tenants[id].last_name;
            }

            return ''
        } else {
            return ''
        }
    }

    getMaxPrice = (number_of_tenants) => {
        if(number_of_tenants === 1) {
            return 4000;
        } else if (number_of_tenants < 4) {
            return (number_of_tenants * 3) * 1000;
        } else {
            return 10000;
        }
    }

    renderNameQuestion() {
        let question_text = "";
        if (this.props.number_of_tenants <= 1) {
            question_text = "What <span> is your name</span>?"
        } else {
            question_text = "What <span> are your names</span>?"
        }
        return (
            <div className="survey-question" id="tenant_names">
                <SurveyQuestionHeader
                    surveyQuestion={question_text}
                    hasHelp={true}
                    surveyQuestionHelpText={`Please add the names of the people you are going to live with.\n
                    You will be able to change the names of your roommates at any time on the survey snapshot section of the tour setup page later on.`}
                />
                <span className="col-md-12 survey-error-message" id="name_of_tenants_error"></span>
                <div className="name-input-wrapper">
                    <input type="text"
                           className="col-md-6 survey-input"
                           name="roommate_name_0"
                           placeholder={'My First Name'}
                           data-tenantkey={0}
                           defaultValue={''}
                           value={this.setNameOnField(0, 'first')}
                           onChange={(e) => this.props.onHandleTenantName(e, 'first')}
                    />
                    <input type="text"
                           className="col-md-6 survey-input"
                           name="roommate_name_0"
                           placeholder={'My Last Name'}
                           data-tenantkey={0}
                           defaultValue={''}
                           value={this.setNameOnField(0, 'last')}
                           onChange={(e) => this.props.onHandleTenantName(e, 'last')}
                    />
                </div>
                {this.props.number_of_tenants > 1 && Array.from(Array(this.props.number_of_tenants - 1)).map((t, i) => {
                    return (
                        <div key={i} className="name-input-wrapper">
                            <input type="text"
                               className="col-md-6 survey-input"
                               name={`roommate_name_${i + 1}`}
                               placeholder={`Roommate #${i + 1} First Name`}
                               data-tenantkey={i + 1}
                               value={this.setNameOnField(i+1, 'first')}
                               onChange={(e) => this.props.onHandleTenantName(e, 'first')}
                            />
                            <input type="text"
                               className="col-md-6 survey-input"
                               name={`roommate_name_${i + 1}`}
                               placeholder={`Roommate #${i + 1} Last Name`}
                               data-tenantkey={i + 1}
                               value={this.setNameOnField(i+1, 'last')}
                               onChange={(e) => this.props.onHandleTenantName(e, 'last')}
                            />
                        </div>
                    );
                })}
            </div>
        );
    }

    renderHomeTypeQuestion() {
        if(this.state.home_type_options) {
            return (
                <div className="survey-question" onChange={this.validateHomeType}>
                    <h2>What <span>kind of home</span> do you want? <span className="checkbox-helper-text">(Select all that apply)</span></h2>
                    <span className="col-md-12 survey-error-message" id="home_type_error"></span>
                    {this.state.home_type_options.map((o, index) => (
                        <label className="col-md-6 survey-label survey-checkbox" key={index} onChange={(e) => this.props.setHomeTypes(e, index, o.id)}>
                            <input type="checkbox" name="home_type" value={o.id} checked={this.props.generalInfo.home_type.length && this.props.generalInfo.home_type.some(i => i === o.id)} onChange={() => {}} />
                            <div>{o.home_type} <i className="material-icons">check</i></div>
                        </label>
                    ))}
                </div>

            );
        }
    }

    renderPriceQuestion() {
        return(
            <div className="survey-question">
                <SurveyQuestionHeader
                    surveyQuestion={`How much rent do you <span>want to pay</span>?`}
                    hasHelp={true}
                    surveyQuestionHelpText={`Please select the desired price range as the total price per month for the apartment.\n
                    The left dot is your desired price, i.e how much you would like to spend.
                    The right dot is your maximum price, i.e the max you are willing to spend on an apartment.`}
                />
                <small id="priceHelp" className="form-text text-muted">Please select your desired price with the left dot and the maximum price you are willing to pay with the right
                </small>
                <span className="col-md-12 survey-error-message" id="price_error"></span>
                <InputRange
                    draggableTrack={false}
                    maxValue={this.getMaxPrice(this.props.number_of_tenants)}
                    minValue={0}
                    step={50}
                    value={{min: this.props.generalInfo.desired_price, max: this.props.generalInfo.max_price}}
                    onChange={value => {this.setState({value});this.props.setPrice(this.state.value.min, this.state.value.max);}}
                    formatLabel={value => `$${value}`} />
            </div>
        );
    }

    renderPriceWeightQuestion() {
        return (
            <div className="survey-question" onChange={(e) =>this.props.onGeneralInputChange(e, 'number')}>
                <SurveyQuestionHeader
                    surveyQuestion={'How <span>important is the price</span>?'}
                />
                <span className="col-md-12 survey-error-message" id="price_weight_error"></span>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="0" checked={this.props.generalInfo.price_weight === 0} onChange={() => {}} />
                    <div>Don’t care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="1" checked={this.props.generalInfo.price_weight === 1} onChange={() => {}} />
                    <div>Slightly care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="2" checked={this.props.generalInfo.price_weight === 2} onChange={() => {}} />
                    <div>Care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="3" checked={this.props.generalInfo.price_weight === 3} onChange={() => {}} />
                    <div>Really care</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="4" checked={this.props.generalInfo.price_weight === 4} onChange={() => {}} />
                    <div>Super important</div>
                </label>
                <label className="col-md-4 survey-label">
                    <input type="radio" name="price_weight" value="5" checked={this.props.generalInfo.price_weight === 5} onChange={() => {}} />
                    <div>Top priority!</div>
                </label>
            </div>
        );
    }

    renderUrgencyQuestion() {
        return(
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <SurveyQuestionHeader
                    surveyQuestion={`How badly do you <span>need to find</span> an apartment?`}
                    hasHelp={true}
                    surveyQuestionHelpText={`Please select how badly you need to move:\n
                    Just browsing: Just seeing what is currently on market\n
                    I've got some time: I am looking to go on tours/sign sometime in the near future but I am in no rush.\n
                    Looking to sign: I am looking to go on tours/sign on an apartment.\n
                    I gotta move ASAP: I am looking to go on tours/sign on an apartment and I am looking to move in as soon as I can.`}
                />
                <span className="col-md-12 survey-error-message" id="move_weight_error"></span>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="0" checked={this.props.generalInfo.move_weight === 0} onChange={() => {}} />
                    <div>Just browsing</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="1" checked={this.props.generalInfo.move_weight === 1} onChange={() => {}} />
                    <div>{this.props.number_of_tenants === 1 ? "I've" : "We've"} got some time</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="2" checked={this.props.generalInfo.move_weight === 2} onChange={() => {}} />
                    <div>Looking to sign</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="move_weight" value="3" checked={this.props.generalInfo.move_weight === 3} onChange={() => {}} />
                    <div>{this.props.number_of_tenants === 1 ? "I" : "We"} gotta move ASAP!</div>
                </label>
            </div>
        );
    }

    renderDatePickingQuestion() {
        if (this.props.generalInfo.move_weight !== 3) {
            return (
                <div className="survey-question">
                    <h2>When do you want to <span>move in</span>?</h2>
                    <span className="col-md-12 survey-error-message" id="date_error"></span>
                    <div className="col-md-6 date-wrapper">
                        <span className="date-info">
                            Earliest You'd like to move in: {!this.props.generalInfo.earliest_move_in ? '(Select a date below.)' : this.props.generalInfo.earliest_move_in.format('MM/DD/YYYY')}
                        </span>
                        <DayPicker
                            onDayClick={this.props.handleEarliestClick}
                            selectedDays={!this.props.generalInfo.earliest_move_in ? null : new Date(this.props.generalInfo.earliest_move_in)}
                            initialMonth={!this.props.generalInfo.earliest_move_in ? new Date() : new Date(this.props.generalInfo.earliest_move_in)}
                        />
                    </div>
                    <div className="col-md-6 date-wrapper">
                        <span className="date-info">
                            Latest You'd like to move in: {!this.props.generalInfo.latest_move_in ? '(Select a date below.)' : this.props.generalInfo.latest_move_in.format('MM/DD/YYYY')}
                        </span>
                        <DayPicker
                            onDayClick={this.props.handleLatestClick}
                            selectedDays={!this.props.generalInfo.latest_move_in ? null : new Date(this.props.generalInfo.latest_move_in)}
                            initialMonth={!this.props.generalInfo.latest_move_in ? new Date() : new Date(this.props.generalInfo.latest_move_in)}
                        />
                    </div>
                </div>
            );
        } else {
            return null
        }
    }

    renderBedroomQuestion() {
        return(
            <div className="survey-question" onChange={this.setRoomChoices}>
                <h2>How many <span>bedrooms</span> do you need? <span className="checkbox-helper-text">(Select all that apply)</span></h2>
                <span className="col-md-12 survey-error-message" id="number_of_rooms_error"></span>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="num_bedrooms" value="0" checked={this.props.generalInfo.num_bedrooms.some(i => i === 0)} onChange={() => {}} />
                    <div>Studio <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="num_bedrooms" value="1" checked={this.props.generalInfo.num_bedrooms.some(i => i === 1)} onChange={() => {}} />
                    <div>1 bed <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="num_bedrooms" value="2" checked={this.props.generalInfo.num_bedrooms.some(i => i === 2)} onChange={() => {}} />
                    <div>2 beds <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="num_bedrooms" value="3" checked={this.props.generalInfo.num_bedrooms.some(i => i === 3)} onChange={() => {}} />
                    <div>3 beds <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="num_bedrooms" value="4" checked={this.props.generalInfo.num_bedrooms.some(i => i === 4)} onChange={() => {}} />
                    <div>4 beds <i className="material-icons">check</i></div>
                </label>
                <label className="col-md-6 survey-label survey-checkbox">
                    <input type="checkbox" name="num_bedrooms" value="5" checked={this.props.generalInfo.num_bedrooms.some(i => i === 5)} onChange={() => {}} />
                    <div>5 beds <i className="material-icons">check</i></div>
                </label>
            </div>
        );
    }

    setRoomChoices = (e) => {
        const value = parseInt(e.target.value);
        let room_choice = this.props.generalInfo.num_bedrooms;
        if (e.target.checked) {
            room_choice.push(value);
            this.props.handleNumberOfRooms(room_choice);
        } else {
            for (let i = 0; i < room_choice.length; i++) {
                if (room_choice[i] === value) {
                    room_choice.splice(i, 1);
                    this.props.handleNumberOfRooms(room_choice);
                }
            }
        }
    }

    handleNextButtonAction(e) {
        /**
         * Handles pressing the next button to make sure the section is valid
         *  before allowing the user to continue
         */
        if (this.handleValidation()) {
            this.props.handleNextStep(e)
        }
    }

    renderGoogleMaps() {
        /**
         * Renders the correct google map depending on the type of filtering the user wants
         */

        // 1 is draw on map
        if (this.props.generalInfo.polygon_filter_type === 1) {
            return (
                <>
                    <small className="form-text text-muted">
                        Please click and drag to move map. Click to add points. Add as many points per shape. Add as many shapes as you want.
                    </small>
                    {this.props.googleApiLoaded ?
                        <MyMapComponent
                            onCompletePolygon={this.props.onCompletePolygon}
                            polygons={this.props.generalInfo.polygons}
                        />
                        :
                        null
                    }
                    <button className="survey-btn filter-delete-button" onClick={this.props.onDeleteAllPolygons}>Delete all areas</button>
                </>
            );

        // If the user does not want to draw then make the component null
        } else {
            return null;
        }

    }

    renderFilterQuestion() {
        /**
         * Renders the question for the map filter
         */
        return (
            <div className="survey-question" onChange={(e) => this.props.onGeneralInputChange(e, 'number')}>
                <SurveyQuestionHeader
                    surveyQuestion={`Do you have <span>areas</span> where you would like to live?`}
                    hasHelp={true}
                    surveyQuestionHelpText={`If you know of certain areas you would want to live in, please select "Draw on Map" and draw the shapes on the map.\n
                    Please select areas you would like to live by drawing shapes on the map. You may draw as many shapes as you like.
                    The only requirement is to have at least 3 points and close the shape by clicking on the start point. The homes will be chosen within all the shapes you draw.`}
                />
                <label className="col-md-6 survey-label">
                    <input type="radio" name="polygon_filter_type" value="1" checked={this.props.generalInfo.polygon_filter_type === 1}
                           onChange={() => {
                           }}/>
                    <div>Draw on map</div>
                </label>
                <label className="col-md-6 survey-label">
                    <input type="radio" name="polygon_filter_type" value="0" checked={this.props.generalInfo.polygon_filter_type === 0} />
                    <div>I am looking everywhere</div>
                </label>
            </div>
        );
    }

    renderFilterZones() {
        return (
            <>
                {this.renderFilterQuestion()}
                {this.renderGoogleMaps()}
            </>
        );

    }



    render() {
        return (
            <>
                {!this.props.is_editing ? this.renderNumberOfPeopleQuestion() : null}
                {!this.props.is_editing ? this.renderNameQuestion() : null}
                {this.renderHomeTypeQuestion()}
                {this.renderPriceQuestion()}
                {this.renderPriceWeightQuestion()}
                {this.renderFilterZones()}
                {this.renderUrgencyQuestion()}
                {this.renderDatePickingQuestion()}
                {this.renderBedroomQuestion()}

                <div className="row survey-btn-wrapper">
                    <button className="col-md-12 survey-btn" onClick={(e) => this.handleNextButtonAction(e)} >
                        Next
                    </button>
                </div>
            </>
        );
    }
}

const defaultMapOptions = {
    // Disables the other types of maps, i.e satellite etc
    mapTypeControlOptions: {
        mapTypeIds: []
    },

    gestureHandling: 'cooperative',

    // Disables street view
    streetViewControl: false,

    styles: [
            {
                "featureType": "all",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "color": "#5b6571"
                    },
                    {
                        "lightness": "35"
                    }
                ]
            },
            {
                "featureType": "administrative.neighborhood",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "landscape",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#f3f4f4"
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "geometry",
                "stylers": [
                    {
                        "weight": 0.9
                    },
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#83cead"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#fee379"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    },
                    {
                        "color": "#7fc8ed"
                    }
                ]
            }
        ],
};

const MyMapComponent = compose(
    withProps({
        loadingElement: <div style={{height: `100%`}}/>,
        containerElement: <div style={{height: `400px`}}/>,
        mapElement: <div style={{height: `100%`}}/>,
    }),
    withGoogleMap
)(props => (
    <GoogleMap
        defaultZoom={11}
        defaultCenter={{lat: 42.3601, lng: -71.0589}}
        defaultOptions={defaultMapOptions}
    >

        {/* Draws all the polygons stored in the state */}
        {props.polygons.map(p =>
                <Polygon
                    key={p.key}
                    path={p.vertices}
                    options={{
                        fillColor: '#008080',
                        strokeColor: '#a13718',
                        fillOpacity: .5,
                        strokeOpacity: .8,
                        strokeWeight: 5,
                        editable: true,
                        zIndex: 1,
                    }}
                />
        )}

        <DrawingManager
            /* Contains all the configuration for the google drawing manager */
            defaultDrawingMode={google.maps.drawing.OverlayType.POLYGON}
            defaultOptions={{
                drawingControl: false,
                drawingControlOptions: {
                    drawingModes: [
                        google.maps.drawing.OverlayType.POLYGON,
                    ],
                },
                polygonOptions: {
                    fillColor: '#008080',
                    strokeColor: '#a13718',
                    fillOpacity: .5,
                    strokeOpacity: .8,
                    strokeWeight: 5,
                    editable: true,
                    zIndex: 1,
                },
            }}
            onPolygonComplete={props.onCompletePolygon}
        />

    </GoogleMap>
));

