import { Configuration, PopupRequest } from "@azure/msal-browser";

export const msalConfig: Configuration = {
    auth: {
        clientId: process.env.REACT_APP_MSAL_CLIENT_ID || "",
        authority: process.env.REACT_APP_MSAL_AUTHORITY,
        redirectUri: window.location.origin,
    },
    cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false,
    },
};

export const loginRequest: PopupRequest = {
    scopes: ["user.read"],
};