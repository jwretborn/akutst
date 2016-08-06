import React from 'react';
import ReactDOM from 'react-dom';
import PatientForm from './components/patient-form.js';
import ProcedureForm from './components/procedure-form.js';
import DiagnosticProcedureList from './components/diagnostic-procedure-list.js';

if (document.getElementById('patients-react') !== null) {
	ReactDOM.render(<PatientForm />, document.getElementById('patients-react'));
}
if (document.getElementById('procedure-react') !== null) {
	ReactDOM.render(<ProcedureForm />, document.getElementById('procedure-react'));
}
if (document.getElementById('diagnostic-procedure-list') !== null) {
	ReactDOM.render(<DiagnosticProcedureList />, document.getElementById('diagnostic-procedure-list'));
}
