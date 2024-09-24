import { Configuration, PopupRequest } from "@azure/msal-browser";

const getRedirectUri = () => {
    const origin = window.location.origin;
    console.log("Redirect URI:", origin);
    return origin;
};

export const msalConfig: Configuration = {
    auth: {
        clientId: process.env.REACT_APP_MSAL_CLIENT_ID || "",
        authority: process.env.REACT_APP_MSAL_AUTHORITY,
        redirectUri: getRedirectUri(),
    },
    cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false,
    },
};

export const loginRequest: PopupRequest = {
    scopes: ["user.read"],
};

console.log("Redirect Config:", JSON.stringify(msalConfig, null, 2));