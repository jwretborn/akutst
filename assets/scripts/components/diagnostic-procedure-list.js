import React, { Component } from 'react';
import ApiStore from '../stores/api-store.js';

export default class DiagnosticProcedureList extends Component {

	constructor(props) {
		super(props);

		this.state = {
            'listItems' : []
		}

        this.handleStoreChange = this.handleStoreChange.bind(this);
	}

    // Do initial loading
    componentWillMount() {
        ApiStore.addChangeListener(this.handleStoreChange);
        this.loadData();
    }

    componentWillUnmount() {
        ApiStore.removeChangeListener(this.handleStoreChange);
    }

    loadData() {
        var data = ApiStore.get(this.props.url);
        if (data !== 'loading') {
            this.setState({
                listItems : data.items
            })
        }
    }

    handleStoreChange() {
		this.loadData();
	}

	render() {
		return (
			<ul>
            { this.state.listItems.map(function(procedure) {
            return (
                <li>
                    {procedure['id']}
                </li>
                )
            }.bind(this))}
			</ul>
		);
	}
}

DiagnosticProcedureList.defaultProps = {
    url				: 'diagnostics/procedures'
}
