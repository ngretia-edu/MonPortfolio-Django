// /static/js/app.jsx - Version compatible avec tes views.py
const { useState, useEffect } = React;

function Portfolio() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadPortfolioData();
    }, []);

    const loadPortfolioData = async () => {
        try {
            setLoading(true);
            const response = await axios.get('/api/portfolio/');
            
            if (response.data.success) {
                setData(response.data);
                setError(null);
            } else {
                setError(response.data.error || 'Erreur lors du chargement');
            }
        } catch (err) {
            console.error('Erreur:', err);
            setError('Impossible de charger les données du portfolio');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="d-flex justify-content-center align-items-center" style={{minHeight: '100vh'}}>
                <div className="text-center">
                    <div className="spinner-border text-primary mb-3" role="status">
                        <span className="visually-hidden">Chargement...</span>
                    </div>
                    <p>Chargement du portfolio...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container-fluid bg-danger text-white d-flex align-items-center justify-content-center" style={{minHeight: '100vh'}}>
                <div className="text-center">
                    <i className="fas fa-exclamation-triangle fa-4x mb-4"></i>
                    <h1>Erreur de chargement</h1>
                    <p className="lead">{error}</p>
                    <button className="btn btn-light" onClick={loadPortfolioData}>
                        <i className="fas fa-redo me-2"></i>Réessayer
                    </button>
                </div>
            </div>
        );
    }

    if (!data || !data.profile) {
        return (
            <div className="container-fluid bg-warning text-dark d-flex align-items-center justify-content-center" style={{minHeight: '100vh'}}>
                <div className="text-center">
                    <i className="fas fa-info-circle fa-4x mb-4"></i>
                    <h1>Aucun profil trouvé</h1>
                    <p className="lead">Veuillez créer un profil dans l'interface d'administration.</p>
                    <a href="/admin/" className="btn btn-dark">
                        <i className="fas fa-cog me-2"></i>Aller à l'admin
                    </a>
                </div>
            </div>
        );
    }

    const { profile, competences, projets, experiences } = data;

    return (
        <div>
            {/* Header */}
            <header className="bg-primary text-white text-center py-5">
                <div className="container">
                    {profile.photo && (
                        <img 
                            src={profile.photo} 
                            alt={profile.nom}
                            className="rounded-circle mb-3"
                            style={{width: '150px', height: '150px', objectFit: 'cover'}}
                        />
                    )}
                    <h1 className="display-4 fw-bold">{profile.nom}</h1>
                    <p className="lead">{profile.titre}</p>
                    <p>{profile.bio}</p>
                    
                    {/* Liens sociaux */}
                    <div className="mt-4">
                        {profile.linkedin && (
                            <a href={profile.linkedin} className="text-white me-3" target="_blank">
                                <i className="fab fa-linkedin fa-2x"></i>
                            </a>
                        )}
                        {profile.github && (
                            <a href={profile.github} className="text-white me-3" target="_blank">
                                <i className="fab fa-github fa-2x"></i>
                            </a>
                        )}
                        {profile.twitter && (
                            <a href={profile.twitter} className="text-white me-3" target="_blank">
                                <i className="fab fa-twitter fa-2x"></i>
                            </a>
                        )}
                        {profile.website && (
                            <a href={profile.website} className="text-white me-3" target="_blank">
                                <i className="fas fa-globe fa-2x"></i>
                            </a>
                        )}
                    </div>
                </div>
            </header>

            {/* Compétences */}
            {competences.length > 0 && (
                <section className="py-5">
                    <div className="container">
                        <h2 className="text-center mb-5">Mes Compétences</h2>
                        <div className="row">
                            {competences.map(competence => (
                                <div key={competence.id} className="col-md-6 col-lg-4 mb-4">
                                    <div className="card h-100">
                                        <div className="card-body">
                                            <div className="d-flex align-items-center mb-3">
                                                {competence.icone && (
                                                    <i className={`${competence.icone} fa-2x me-3`} 
                                                       style={{color: competence.couleur}}></i>
                                                )}
                                                <div>
                                                    <h5 className="card-title mb-1">{competence.nom}</h5>
                                                    <small className="text-muted">{competence.categorie_display}</small>
                                                </div>
                                            </div>
                                            <div className="progress">
                                                <div className="progress-bar" 
                                                     style={{width: `${competence.niveau}%`, backgroundColor: competence.couleur}}>
                                                    {competence.niveau}%
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            )}

            {/* Projets */}
            {projets.length > 0 && (
                <section className="py-5 bg-light">
                    <div className="container">
                        <h2 className="text-center mb-5">Mes Projets</h2>
                        <div className="row">
                            {projets.map(projet => (
                                <div key={projet.id} className="col-md-6 col-lg-4 mb-4">
                                    <div className="card h-100">
                                        {projet.image_principale && (
                                            <img src={projet.image_principale} 
                                                 className="card-img-top" 
                                                 alt={projet.titre}
                                                 style={{height: '200px', objectFit: 'cover'}} />
                                        )}
                                        <div className="card-body">
                                            <h5 className="card-title">{projet.titre}</h5>
                                            <p className="card-text">{projet.description_courte}</p>
                                            
                                            {/* Technologies */}
                                            <div className="mb-3">
                                                {projet.technologies.map((tech, index) => (
                                                    <span key={index} className="badge me-1" 
                                                          style={{backgroundColor: tech.couleur}}>
                                                        {tech.nom}
                                                    </span>
                                                ))}
                                            </div>
                                            
                                            {/* Liens */}
                                            <div className="d-flex gap-2">
                                                {projet.url_demo && (
                                                    <a href={projet.url_demo} className="btn btn-primary btn-sm" target="_blank">
                                                        <i className="fas fa-eye me-1"></i>Demo
                                                    </a>
                                                )}
                                                {projet.url_code && (
                                                    <a href={projet.url_code} className="btn btn-outline-primary btn-sm" target="_blank">
                                                        <i className="fab fa-github me-1"></i>Code
                                                    </a>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            )}

            {/* Contact */}
            <section className="py-5">
                <div className="container">
                    <div className="row justify-content-center">
                        <div className="col-md-8 text-center">
                            <h2 className="mb-4">Me Contacter</h2>
                            <p className="lead mb-4">{profile.description_longue}</p>
                            <div className="d-flex justify-content-center gap-3">
                                <a href={`mailto:${profile.email}`} className="btn btn-primary">
                                    <i className="fas fa-envelope me-2"></i>Email
                                </a>
                                {profile.telephone && (
                                    <a href={`tel:${profile.telephone}`} className="btn btn-outline-primary">
                                        <i className="fas fa-phone me-2"></i>Téléphone
                                    </a>
                                )}
                                {profile.cv && (
                                    <a href={profile.cv} className="btn btn-success" target="_blank">
                                        <i className="fas fa-download me-2"></i>Télécharger CV
                                    </a>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

// Rendu de l'application
ReactDOM.render(<Portfolio />, document.getElementById('root'));