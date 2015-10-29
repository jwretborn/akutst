import React from 'react';
import DynamicSearch from './dynamic_search.js';

React.render(<DynamicSearch url={ '/api/codes' } mapBadge={'type'} name={'retts'} nameDisplay={'Sökorsak'} />, document.getElementById('retts-react'));