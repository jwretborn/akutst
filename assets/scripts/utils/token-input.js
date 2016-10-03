import React, { Component } from 'react';
import ApiStore from '../stores/api-store.js';
import TokenAutocomplete from 'react-token-autocomplete';

export default class TokenInput extends Component {

	constructor(props) {
		super(props);
		this.state = {
			selectValue		: '',
			listItems		: [],
			selected 		: []
		};

	}

	render() {
		return (
			<div>
				<TokenAutocomplete
					placeholder="type to limit suggestions"
					defaultValues={['apple']}
					options={['apple', 'banana', 'carrot', 'watermelon']}
					/>
 			</div>
		)
	}
}

TokenInput.defaultProps = {
	name 		: '',
	label 		: 'Select',
	mapKey 		: 'id',
	mapValue	: 'name',
	url			: '',
	onUpdate	: ''
}
