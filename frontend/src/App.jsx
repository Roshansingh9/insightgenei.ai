import Header from "./components/Header";
import CustomFooter from "./components/Footer";
import QueryInterface from "./components/Maincomponent";

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-[#0a0a0a] overflow-x-hidden">
      <Header />

      <main className="flex-1 pt-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full text-white">
        <QueryInterface />
      </main>

      <CustomFooter />
    </div>
  );
}

export default App;
