import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';

const boxStyle = {
    paddingTop: 15,
    paddingBottom: 35,
    display: 'flex',
    justifyContent: 'center',
};

class AutocompleteUI extends Component{

render(){
return (
    <div style={boxStyle}>
    <Autocomplete
        id="stock-autocomplete"
        options={this.props.top100stocks}
        getOptionLabel={option => option.name}
        style={{ width: 350 }}
        onKeyDown={this.props.keySubmit}
        renderInput={params => (
            <TextField {...params} label="Search by name" variant="outlined" fullWidth />
            
        )}
    />
    </div>
);
}
}

export default AutocompleteUI;