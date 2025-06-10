import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Typography } from '@mui/material';

const Navigation: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          TAO Galaxy
        </Typography>
        <Button color="inherit" component={Link} to="/">
          Subnet Explorer
        </Button>
        <Button color="inherit" component={Link} to="/analytics">
          Analytics Dashboard
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation; 