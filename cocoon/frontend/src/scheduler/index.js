// Import React Components
import React from 'react';
import ReactDOM from "react-dom";
import ClientScheduler from "./clientScheduler/clientScheduler";
import AgentScheduler from "./agentScheduler/agentScheduler";

// Determines which component to load via dictionary
//  This should be passed in the context to the template
const components = {
    'ClientScheduler': ClientScheduler,
    'AgentScheduler': AgentScheduler,
};

ReactDOM.render(
    React.createElement(components[window.component], window.props),
    window.react_mount
);
