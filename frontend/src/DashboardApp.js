import React, { Component } from "react";
import { w3cwebsocket as W3CWebSocket } from "websocket";

import Container from "@material-ui/core/Container";

import { withStyles } from "@material-ui/core/styles";
import {LineChart} from "@mui/x-charts";
import {Grid} from "@material-ui/core";

const useStyles = (theme) => ({
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
});

function getUserId() {
  return Math.random().toString()
}

function valueFormatter(value) {
  const date = new Date(value * 1000)
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric'};
  return new Intl.DateTimeFormat('en-US', options).format(date);
}

class DashboardApp extends Component {
  state = {
    measurementAlerts: [], // [{xData: [], yData: [], xLabel, yLabel}]
  };

  clientMeasurementAlerts = new W3CWebSocket("ws://0.0.0.0:8000/ws/measurements/" + getUserId() + "/");

  onButtonClicked = (e) => {
    // TODO: to another page
    e.preventDefault();
  };

  componentDidMount() {
    this.clientMeasurementAlerts.onopen = () => {
      console.log("WebSocket Measurement Client Connected");
    };

    this.clientMeasurementAlerts.onmessage = (message) => {
      const dataFromServer = JSON.parse(message.data);
      if (dataFromServer) {
        console.log("dataFromServer:", dataFromServer);

        this.setState((state) => ({
          measurementAlerts: dataFromServer,
        }));
      }
    };

  }

  render() {
    const { classes } = this.props;
    return (
        <Container component="main" >
          Dashboards
          <Grid container spacing={2}>
            {this.state.measurementAlerts.map((measurementAlert) => (
              <Grid item xs={6}>
                <LineChart
              xAxis={[{
                data: measurementAlert.xData,
                label: measurementAlert.xLabel,
                valueFormatter: (v) => valueFormatter(v),
              }]}
              series={[
                {
                  data: measurementAlert.yData,
                  label: measurementAlert.yLabel,
                },
              ]}
              width={500}
              height={300}
            />
              </Grid>
            ))}
        </Grid>
      </Container>
    );
  }
}
export default withStyles(useStyles)(DashboardApp);
