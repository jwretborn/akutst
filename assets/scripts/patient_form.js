import React, { Component } from 'react';
import DynamicSearch from './dynamic_search.js';
import InputSelect from './input_select.js';

export default class PatientForm extends Component {

	constructor(props) {
		super(props);
		var d = new Date();

		this.state = {
			searchFilter 	: 'adult',
			date 			: d.toISOString().substring(0, 10),
			user_id 		: false
		}

		this.handleSelectChange = this.handleSelectChange.bind(this);
		this.handleFieldChange = this.handleFieldChange.bind(this);
	}

	componentWillMount() {

	}

	handleFieldChange(field) {
		return function(event) {
			var elem = (typeof event.selectedIndex === "undefined" ? event.target : event);
    		var value = elem.value || elem.options[elem.selectedIndex].value;
			var newState = {};
			newState[field] = value;

    		this.setState(newState);
    	}.bind(this);
	}

	handleSelectChange(key, value, namespace) {
		switch (namespace) {
			case 'age' :
				if (value !== 'Vuxen') {
					this.setState({searchFilter : 'ped'});
				}
				else {
					this.setState({searchFilter : 'adult'});
				}
				break;
			default :
				break;
		}
	}

	render() {
		return (
			<div>
				<div className="form-group">
					<label htmlFor="id" className="col-sm-2 control-label">Användare</label>
					<div className="col-sm-4">
						<input
							type 		=	"text"
							className 	=	"form-control"
							name 		=	"user_id"
							onBlur		=	{ this.handleFieldChange('user_id') } />
					</div>
				</div>
				<div className="form-group">
					<label htmlFor="date" className="col-sm-2 control-label">Datum</label>
					<div className="col-sm-4">
						<input
							type 		= 	"date"
							className 	=	"form-control"
							name 		= 	"date"
							defaultValue=	{ this.state.date }
							onBlur 		=	{ this.handleFieldChange('date') } />
					</div>
				</div>
				<div className="form-group">
					<InputSelect
						url			=	{ 'group/colours/items' }
						name 		=	{ 'prio' }
						onUpdate	=	{ this.handleSelectChange } />
				</div>
				<div className="form-group">
					<InputSelect
						url 	 	=	{ 'group/ages/items' }
						name 	 	= 	{ 'age' }
						onUpdate 	=	{ this.handleSelectChange } />
				</div>
				<div className="form-group">
					<DynamicSearch
						url 		= 	{ 'codes' }
						mapBadge 	=	{ 'type' }
						name 		=	{ 'retts' }
						nameDisplay =	{ 'Sökorsak' }
						filterKey 	=	{ 'type' }
						filterValue =	{ this.state.searchFilter } />
				</div>
				<div className="form-group">
					<label htmlFor="admittance" className="col-sm-2 control-label">Inläggning</label>
					<div className="col-sm-4">
					    <label className="radio-inline">
					        <input type="radio" name="admittance" id="admittancelRadio1" value="1" /> Ja
					    </label>
					    <label className="radio-inline">
					        <input type="radio" name="admittance" id="admittancelRadio2" value="0" /> Nej
					    </label>
					</div>
				</div>
				<div className="form-group">
					<label htmlFor="tuition" className="col-sm-2 control-label">Handledning</label>
					<div className="col-sm-4">
						<label className="radio-inline">
							<input type="radio" name="tuition" id="tuitionlRadio1" value="1" /> Ja
						</label>
						<label className="radio-inline">
							<input type="radio" name="tuition" id="tuitionlRadio2" value="0" /> Nej
						</label>
					</div>
				</div>
				<div className="form-group">
					<label htmlFor="comments" className="col-sm-2 control-label">Kommentar</label>
					<div className="col-sm-4">
						<input type="text" className="form-control" name="comments" />
					</div>
				</div>
				<div className="form-group">
					<div className="col-sm-2"></div>
					<div className="col-sm-4">
						<input className="btn btn-default" type="submit" value="Submit" />
					</div>
				</div>
			</div>
		);
	}
}

PatientForm.defaultProps = {

}
