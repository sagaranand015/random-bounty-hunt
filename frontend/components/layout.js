import Link from 'next/link'
import { useAuth } from '../utils/authProvider.js';

const shortenAddress = (address) => {
    if (address)
        return address.substring(0, 6) + "..." + address.substring(address.length - 4, address.length)
}

export default function Layout({ children }) {

    const { currentAccount, setCurrentAccount } = useAuth()

    return (
        <div className="h-screen p-6">
            <div>
                <header className="flex justify-between mb-6">
                    <div className="flex items-center">
                        <h3 className="text-xl font-extrabold"><Link href="/">Random Bounty Hunt</Link></h3>
                        {currentAccount && <p className="ml-8 text-gray-600"><Link href="/dashboard">Dashboard</Link></p>}
                    </div>
                    {currentAccount ? (
                        <h4>{shortenAddress(currentAccount)}</h4>
                    ) : (
                        <button className="px-4 py-2 text-lg border border-orange-600 text-orange-600" onClick={setCurrentAccount}>Connect Wallet</button>
                    )}
                </header>
                <main>
                    {children}
                </main>
            </div>

            <footer>
                <div className="mt-8 mb-6 border border-grey-600"></div>
                <div className="flex justify-between">
                    <p>Life is in this moment. There is no other meaning of life.</p>
                </div>
            </footer>
        </div>
    )
}