import React, { Component } from 'react';
import DynamicSearch from './dynamic_search.js';
import InputSelect from './input_select.js';

export default class PatientForm extends Component {

	constructor(props) {
		super(props);
		var d = new Date();

		this.state = {
			searchFilter : '',
			date : d.toISOString().substring(0, 10)
		}

		this.handleSelectChange = this.handleSelectChange.bind(this);
	}

	componentWillMount() {

	}

	handleSelectChange(key, value, name) {
		switch (name) {
			case 'age' :
				if (value !== 'Vuxen') {
					this.setState({searchFilter : 'ped'});
				}
				else {
					this.setState({searchFilter : ''});
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
					<label for="id" className="col-sm-2 control-label">Användare</label>
					<div className="col-sm-4">
						<input type="text" className="form-control" name="user_id" />
					</div>
				</div>
				<div className="form-group">
					<label for="date" className="col-sm-2 control-label">Datum</label>
					<div className="col-sm-4">
						<input type="date" className="form-control" name="date" defaultValue={ this.state.date } />
					</div>
				</div>
				<div className="form-group">
					<InputSelect 
						url			=	{ 'api/group/colours/items' } 
						name 		=	{ 'prio' } 
						onUpdate	=	{ this.handleSelectChange } />
				</div>
				<div className="form-group">
					<InputSelect 
						url 	 	=	{ '/api/group/ages/items' } 
						name 	 	= 	{ 'age' } 
						onUpdate 	=	{ this.handleSelectChange } />
				</div>
				<div className="form-group">
					<DynamicSearch 
						url 		= 	{ '/api/codes' } 
						mapBadge 	=	{ 'type' } 
						name 		=	{ 'retts' } 
						nameDisplay =	{ 'Sökorsak' } 
						filterKey 	=	{ 'type' } 
						filterValue =	{ this.state.searchFilter } />
				</div>
				<div className="form-group">
					<label for="admittance" className="col-sm-2 control-label">Inläggning</label>
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
					<label for="tuition" className="col-sm-2 control-label">Handledning</label>
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
					<label for="comments" className="col-sm-2 control-label">Kommentar</label>
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