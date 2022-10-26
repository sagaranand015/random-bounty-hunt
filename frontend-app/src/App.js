import WalletConnect from "@walletconnect/client";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";
import algosdk from "algosdk";
import HttpClient from "react-http-client";
import { formatJsonRpcRequest } from "@json-rpc-tools/utils";
import { useState } from 'react';

import logo from './logo.svg';
import './App.css';

const STORE_APP_ID = 116942213;
const STORE_APP_ADDRESS = "PBFBJBKP2D55NZ6FL5SURYR235ZIOP2CRQYWHKU2R3OKUVBBJQTZP6JOYE";

function App() {

  // const [state, setState] = useState({});
  // let [account, setAccount] = useState("");
  // let [apiToken, setApiToken] = useState("");
  let account = null;
  let apiToken = null;

  const connector = new WalletConnect({
    bridge: "https://bridge.walletconnect.org", // Required
    qrcodeModal: QRCodeModal,
  });

  const client = new algosdk.Algodv2("", "https://testnet-api.algonode.cloud", "");

  async function subscribeToEvents() {
    // const { connector } = this.state;
    if (!connector) {
      console.log("======== no connector. Please try again!");
      return;
    }
    connector.on("session_update", async (error, payload) => {
      console.log(`connector.on("session_update")`);
      if (error) {
        throw error;
      }
      const { accounts } = payload.params[0];
      account = accounts;
    });

    connector.on("connect", (error, payload) => {
      console.log(`connector.on("connect")`);
      if (error) {
        throw error;
      }
      console.log("========= onConnect", payload);
      const address = payload.params[0].accounts[0];
      account = address;
      console.log("========= onConnect DONE", payload, address);
    });

    connector.on("disconnect", (error, payload) => {
      console.log(`connector.on("disconnect")`);

      if (error) {
        throw error;
      }
      account = null;
    });

    if (connector.connected) {
      console.log("======= I'm already connected!");
      const { accounts } = connector;
      const address = accounts[0];
      account = address;
    }
  };

  async function ConnectWallet() {
    if (!connector.connected) {
      await connector.createSession();
    }
    // connector.connect();
    await subscribeToEvents();
  };

  async function GetAccountBalance() {

    if (connector.connected) {
      const { accounts } = connector;
      const address = accounts[0];
      console.log("======= connected here too!", accounts, address);
      account = address;
    }

    console.log("========= account balance of address: ", account);
    const accountInfo = await client
      .accountInformation(account)
      .setIntDecoding(algosdk.IntDecoding.BIGINT)
      .do();
    console.log("======== account info is: ", accountInfo);
    console.log("======== account balance is: ", accountInfo.amount);
  }

  async function GetStoreApplication() {
    var resp = await client.getApplicationByID(STORE_APP_ID).do();
    console.log("=========== Application details: ", resp);
  }

  async function GetServerHealth() {
    console.log("========= getting server health..");
    const healthStatus = await HttpClient.get("http://localhost:8080/server/health");
    console.log("======= healthStatus is: ", healthStatus);
    alert(healthStatus)
  }

  async function GetAllDatasets() {
    console.log("========= getting all datasets health..");
    try {
      const allDs = await HttpClient.get("http://localhost:8080/datasets/");
      console.log("======= all datasets are: ", allDs);
      if (allDs.status) {
        alert("Got the datasets. See console for object details");
      } else {
        alert("FAILED API CALL. Please check console", allDs);
      }
    }
    catch (e) {
      alert("COULD NOT REACH BACKEND API. Please check console", e);
    }
  }

  async function RegisterUser() {
    console.log("======= starting user registration...");
    try {
      const registerUser = await HttpClient.post("http://localhost:8080/user/register", { "user_address": account });
      console.log("======= register user response is: ", registerUser);
      if (registerUser.status) {
        alert("User Registration Successful!");
        apiToken = registerUser.token;
        console.log("User Registration Successful!", apiToken);
      } else {
        alert("FAILED API CALL. Please check console", registerUser);
      }
    }
    catch (e) {
      alert("COULD NOT REACH BACKEND API FOR USER REGISTRATION. Please check console", e);
    }
  }

  function ShowApiToken() {
    alert(apiToken);
    console.log("Token is there?!", apiToken);
  }

  async function DoSampling() {
    const selectedDs = "1";
    try {
      const authtoken = "Bearer " + apiToken;
      const sampleResp = await HttpClient.post("http://localhost:8080/sample/", { "dataset_id": selectedDs }, {
        'Authorization': authtoken
      });
      console.log("Sampling REsponse is: ", sampleResp);
      if (sampleResp.status) {
        alert("Sample Response Successful");
      }
      else {
        alert("FAILED API CALL. Please check console", sampleResp);
      }
    } catch (e) {
      alert("SAMPLING API CALL FAILED...");
      console.log("SAMPLE API CALL FAILED", e);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={() => ConnectWallet()}>Connect Wallet</button>
        <button onClick={() => GetAccountBalance()}>Get Account Balance</button>
        <button onClick={() => GetStoreApplication()}>Get Store Application</button>
        <button onClick={() => GetServerHealth()}>Get Server Health</button>
        <button onClick={() => GetAllDatasets()}>Get All Datasets</button>
        <button onClick={() => RegisterUser()}>Register User</button>
        <button onClick={() => ShowApiToken()}>Show API Token</button>
        <button onClick={() => DoSampling()}>Do the Sampling!</button>
      </header>
    </div>
  );
}

export default App;
