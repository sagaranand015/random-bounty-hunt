import React from 'react'
import { useContext } from 'react';
import { useState, useEffect } from 'react';

const AuthContext = React.createContext();

function AuthProvider(props)
{

    const [currentAccount, setCurrentAccount] = useState(null)
    
    const checkWalletIsConnected = async () => {
        const { ethereum } = window
        if (ethereum) {
            const accounts = await ethereum.request({ method: 'eth_accounts' })
            if (accounts.length) {
                setCurrentAccount(accounts[0])
            }
        }
    }

    useEffect(() => {
        checkWalletIsConnected()
    }, [])

    const connectWalletHandler = async () => {
        const { ethereum } = window

        if (!ethereum) {
            alert("Please Install Metamask")
        }

        try {
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' })
            setCurrentAccount(accounts[0])
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <AuthContext.Provider value={{currentAccount,setCurrentAccount:connectWalletHandler}}>
            {props.children}
        </AuthContext.Provider>
    );
}

function useAuth()
{
    const authContext = useContext(AuthContext);
    return {...authContext};
}

export {AuthProvider, useAuth};