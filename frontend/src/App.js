import React, { Component } from "react";
import { w3cwebsocket as W3CWebSocket } from "websocket";

import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import Paper from "@material-ui/core/Paper";

import { withStyles } from "@material-ui/core/styles";
import {LineChart} from "@mui/x-charts";
import {Box, Grid, ImageList, ImageListItem, ImageListItemBar} from "@material-ui/core";

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

class App extends Component {
  state = {
    filledForm: true,  // hardcoded
    messages: [],
    value: "",
    name: "me",
    // room: "foo",  // it uses generated user id
    measurementAlerts: [], // [{xData: [], yData: [], xLabel, yLabel}]
  };

  clientAi = new W3CWebSocket("ws://0.0.0.0:8000/ws/ai-chat/" + getUserId() + "/");
  clientMeasurementAlerts = new W3CWebSocket("ws://0.0.0.0:8000/ws/measurement-alerts/" + getUserId() + "/");

  onButtonClicked = (e) => {
    this.clientAi.send(
      JSON.stringify({
        type: "message",
        text: this.state.value,
        sender: this.state.name,
      })
    );
    this.state.value = "";
    e.preventDefault();
  };

  componentDidMount() {
    this.clientAi.onopen = () => {
      console.log("WebSocket Client Connected");
    };
    this.clientMeasurementAlerts.onopen = () => {
      console.log("WebSocket Measurement Client Connected");
    };

    this.clientAi.onmessage = (message) => {
      const dataFromServer = JSON.parse(message.data);
      if (dataFromServer) {
        this.setState((state) => ({
          messages: [
            ...state.messages,
            {
              msg: dataFromServer.text,
              name: dataFromServer.sender,
            },
          ],
        }));
      }
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
          {this.state.measurementAlerts.length !== 0 ? (
            <Grid
                container
                alignItems="center"
                justifyContent="center"
              >
                <h1>Alert</h1>
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
                          color: "red"
                        },
                      ]}
                      width={500}
                      height={240}
                    />
                  </Grid>
                ))}
              </Grid>
        {this.state.filledForm ? (
          <div style={{ marginTop: 50, width: 700 }}>
            <Paper
              style={{height: 240, maxHeight: 240, overflow: "auto", boxShadow: "none",}}
            >
              {this.state.messages.map((message) => (
                <>
                  <Card className={classes.root}>
                    <CardHeader
                        title={message.name}
                        subheader={message.msg}
                        titleTypographyProps={{variant:'p' }}
                    />
                  </Card>
                </>
              ))}
            </Paper>
            <form
              className={classes.form}
              noValidate
              onSubmit={this.onButtonClicked}
            >
              <TextField id="outlined-helperText" label="Write text"
                variant="outlined"
                value={this.state.value}
                fullWidth
                onChange={(e) => {
                  this.setState({ value: e.target.value });
                  this.value = this.state.value;
                }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
              >
                Send Message
              </Button>
            </form>
          </div>
        ) : (
          <div>
            <CssBaseline />
            <div className={classes.paper}>
              <form
                className={classes.form}
                noValidate
                onSubmit={(value) => this.setState({ filledForm: true })}
              >
                <TextField variant="outlined" margin="normal" required fullWidth label="Room name"
                  name="Room name"
                  autoFocus
                  value={this.state.room}
                  onChange={(e) => {
                    this.setState({ room: e.target.value });
                    this.value = this.state.room;
                  }}
                />
                <TextField variant="outlined" margin="normal" required fullWidth name="sender" label="sender"
                  type="sender"
                  id="sender"
                  value={this.state.name}
                  onChange={(e) => {
                    this.setState({ name: e.target.value });
                    this.value = this.state.name;
                  }}
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  Submit
                </Button>
              </form>
            </div>
          </div>
        )}
            </Grid>
          ) : (
              <Grid
                container
                alignItems="center"
                justifyContent="center"
              >
                <Grid>
                  <img
                      style={{height: 500}}
                    src={require('./doguu.png')}
                  />
                </Grid>
                <Grid item xs={12}>
                </Grid>
                <Grid>
                  <h1>Everything runs as expected!</h1>
                </Grid>
              </Grid>
          )}
      </Container>
    );
  }
}
export default withStyles(useStyles)(App);
