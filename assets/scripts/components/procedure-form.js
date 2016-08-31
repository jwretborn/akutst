import React, { Component } from 'react';
import DynamicSearch from '../dynamic_search.js';
import InputSelect from '../input_select.js';
import ApiStore from '../stores/api-store.js';

export default class ProcedureForm extends Component {

	constructor(props) {
		super(props);

		var d = new Date();
		var date = d.toISOString().substring(0, 10);

		if (props.date !== false) {
			date = props.date;
		}

		this.state = {
			date 		: date,
			items		: false,
			procedure 	: false
		}

		this.handleStoreChange = this.handleStoreChange.bind(this);
		this.handleProcedureChange = this.handleProcedureChange.bind(this);
	}

	componentWillMount() {
		ApiStore.addChangeListener(this.handleStoreChange);
		this.loadData();
	}

	componentWillUnmount() {
		ApiStore.removeChangeListener(this.handleStoreChange);
	}

	loadData() {
		var data = ApiStore.get('proceduretype');
		if (data !== 'loading') {
			this.setState({
				items 		: data.items,
				procedure 	: ( this.state.procedure === false  ? data.items[0] : this.state.procedure )
			});
		}
	}

	handleStoreChange() {
		this.loadData();
	}

	handleProcedureChange(value, name) {
		switch (name) {
			case 'procedure' :
				for (var i = this.state.items.length - 1; i>=0; i--) {
					if (this.state.items[i].id == value) {
						this.setState({
							procedure : this.state.items[i]
						});
						break;
					}
				}
				break;
			case 'method' :
				break;
			case 'anatomy' :
				break;
			default :
				break;
		}
	}

	render() {
		var divGrpCls = 'form-group',
			labelCls = "col-sm-2 control-label",
			divColCls = "col-sm-4";

		return (
			<div>
				<div className={ this.props.hidePrefilled === true && this.props.userId !== false ? divGrpCls+" hide" : divGrpCls }>
					<label htmlFor="id" className={ labelCls }>Användare</label>
					<div className={ divColCls }>
						<input
							type 		= "user_id"
							className 	= "form-control"
							name 		= "user_id"
						defaultValue= { this.props.userId !== false ? this.props.userId : '' } />
					</div>
				</div>
				<div className={ this.props.hidePrefilled === true && this.props.date !== false ? divGrpCls+" hide" : divGrpCls }>
					<label htmlFor="date" className={ labelCls }>Datum</label>
					<div className={ divColCls }>
						<input
							type 		= "date"
							className 	= "form-control"
							name 		= "date"
						defaultValue= { this.state.date } />
					</div>
				</div>
				<div className="form-group">
					<DynamicSearch
						url 		= 	{ 'proceduretype' }
						name 		=	{ 'procedure' }
						nameDisplay =	{ 'Procedur' }
						changeCallback = { this.handleProcedureChange }/>
				</div>
				{ this.state.procedure !== false && this.state.procedure.method_group !== null &&
					(
						<div className="form-group method">
							<InputSelect
								url			=	{ 'group/'+this.state.procedure.method_group+'/items' }
								name 		=	{ 'method' }
								label 		=	{ 'Metod' }
								onUpdate 	=	{ this.handleSelectChange } />
						</div>
					)
				}
				{ this.state.procedure !== false && this.state.procedure.anatomy_group !== null &&
					(
						<div className={ divGrpCls }>
							<InputSelect
								url			=	{ 'group/'+this.state.procedure.anatomy_group+'/items' }
								name 		= 	{ 'anatomy' }
								label 		= 	{ 'Lokal' }
								onUpdate	= 	{ this.handleSelectChange } />
						</div>
					)
				}
				<div className={ divGrpCls }>
					<label htmlFor="successful" className={ labelCls }>Framgångsrik</label>
					<div className="col-sm-10">
						<label className="radio-inline">
							<input type="radio" name="successful" id="successfullRadio1" value="1" /> Ja
						</label>
						<label className="radio-inline">
							<input type="radio" name="successful" id="successfullRadio2" value="" /> Nej
						</label>
					</div>
				</div>
				<div className={ divGrpCls }>
					<label htmlFor="tuition" className={ labelCls }>Handledning</label>
					<div className="col-sm-10">
						<label className="radio-inline">
							<input type="radio" name="tuition" id="tuitionlRadio1" value="1" /> Ja
						</label>
						<label className="radio-inline">
							<input type="radio" name="tuition" id="tuitionlRadio2" value="" /> Nej
						</label>
					</div>
				</div>
				<div className={ divGrpCls }>
					<label htmlFor="comments" className={ labelCls }>Kommentar</label>
					<div className={ divColCls }>
						<input type="text" className="form-control" name="comments" />
					</div>
				</div>
				<div className={ divGrpCls }>
					<div className="col-sm-2"></div>
					<div className={ divColCls }>
						<input className="btn btn-default" type="submit" value="Submit" />
					</div>
				</div>
			</div>
		);
	}
}

ProcedureForm.defaultProps = {
	date : false,
	userId : false,
	hidePrefilled : false
}
