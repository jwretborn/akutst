import React from 'react';
import ReactDOM from 'react-dom';
import PatientForm from './components/patient-form.js';
import ProcedureForm from './components/procedure-form.js';
import AnalyticsBasic from './components/analytics-basic.js';

if (document.getElementById('patients-react') !== null) {
	ReactDOM.render(<PatientForm />, document.getElementById('patients-react'));
}
if (document.getElementById('procedure-react') !== null) {
	ReactDOM.render(<ProcedureForm />, document.getElementById('procedure-react'));
}
if (document.getElementById('analytics-basic') !== null) {
	ReactDOM.render(<AnalyticsBasic />, document.getElementById('analytics-basic'));
}
