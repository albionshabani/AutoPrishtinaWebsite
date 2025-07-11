import { motion } from 'framer-motion';
import { FiSearch, FiMessageCircle, FiCheckSquare } from 'react-icons/fi';

const Step = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => (
  <div className="text-center">
    <div className="flex items-center justify-center w-16 h-16 mx-auto bg-blue-100 text-blue-600 rounded-full mb-5">
      <div className="text-3xl">{icon}</div>
    </div>
    <h3 className="text-lg font-semibold text-slate-800 mb-2">{title}</h3>
    <p className="text-slate-500 text-sm leading-relaxed">{description}</p>
  </div>
);

export const HowItWorks = () => {
    return (
        <motion.section 
            initial={{ opacity: 0, y: 50 }} 
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
        >
            <div className="bg-white rounded-2xl p-8 lg:p-12 shadow-xl shadow-slate-900/5 border border-slate-100">
                 <div className="text-center max-w-2xl mx-auto mb-16">
                      <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 tracking-tight">Procesi më i thjeshtë në treg</h2>
                      <p className="mt-4 text-lg text-slate-600">Ne e bëjmë blerjen e një makine nga Korea më të lehtë se kurrë më parë.</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-12 lg:gap-16">
                      <Step icon={<FiSearch />} title="1. Gjej & Kërko" description="Përdorni filtrat tanë të fuqishëm për të gjetur makinën perfekte nga inventari ynë i gjerë." />
                      <Step icon={<FiMessageCircle />} title="2. Rezervo në WhatsApp" description="Kontaktoni direkt me ne përmes WhatsApp për të konfirmuar interesimin dhe për të bërë pyetje." />
                      <Step icon={<FiCheckSquare />} title="3. Finalizo & Dërgo" description="Ne kujdesemi për të gjithë logjistikën për të sjellë makinën tuaj të re direkt në Prishtinë." />
                  </div>
            </div>
        </motion.section>
    )
};