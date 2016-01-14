import React from 'react';
import ReactDOM from 'react-dom';
import PatientForm from './patient_form.js';
import ProcedureForm from './procedure-form.js';

if (document.getElementById('patients-react') !== null) {
	ReactDOM.render(<PatientForm />, document.getElementById('patients-react'));
}
if (document.getElementById('procedure-react') !== null) {
	ReactDOM.render(<ProcedureForm />, document.getElementById('procedure-react'));
}
