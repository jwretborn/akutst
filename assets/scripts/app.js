import React, { Component } from 'react';

export default class App extends Component {
	render() {
		return (
			<div>
				<label for="retts" className="col-sm-2 control-label">Search - react</label>
				<div className="col-sm-4">
                	<input type="text" className="form-control" name="react-search" value="sökorsak" />
				</div>
			</div>
		);
	}
}