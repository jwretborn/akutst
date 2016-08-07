import React, { Component } from 'react';
import StatisticsTable from './statistics-table.js';

export default class AnalyticsBasic extends Component {

	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div id="analytics-basic">
   				<StatisticsTable
					name="Procedurer"
					url={'diagnostics/procedures'}
					keys={['id', 'name', 'anatomy_id', 'comments']}
					groupBy={['name']} />
				<StatisticsTable
					name="Patienter"
					url={'diagnostics/patients'}
					keys={['id', 'age', 'retts', 'triage', 'tuition', 'comments']}
					groupBy={['age', 'triage']} />
   			</div>
		);
	}

}

AnalyticsBasic.defaultProps = {
}
