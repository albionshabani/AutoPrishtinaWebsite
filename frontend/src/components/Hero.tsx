import { SearchForm } from './SearchForm';

export function Hero() {
  const heroBackgroundImage = '/assets/hero-bg.jpg'; 

  return (
    <div className="relative">
      <section 
        className="relative h-[450px] flex items-center justify-center text-white bg-cover bg-top"
        style={{ backgroundImage: `url(${heroBackgroundImage})` }}
      >
        <div className="absolute inset-0 bg-black/60" />
        <div className="relative z-10 flex flex-col items-center text-center px-4">
          <h1 className="text-5xl md:text-6xl font-extrabold leading-tight">
            Gjeni Makinën Tuaj të Ëndrrave
          </h1>
          <p className="mt-4 max-w-xl text-lg text-slate-300">
            Ne ofrojmë një përzgjedhje të automjeteve me cilësi të lartë.
          </p>
        </div>
      </section>

      {/* The SearchForm is now perfectly placed and centered */}
      <div className="relative flex justify-center px-4 sm:px-8 lg:px-12 -mt-24 z-20">
        <SearchForm />
      </div>
    </div>
  );
}