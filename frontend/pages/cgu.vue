<template>
  <div class="terms-container">
    <h1>Conditions d’utilisation</h1>

    <p>
      Les présentes conditions d’utilisation régissent l’accès et l’utilisation
      de l’application <strong>PlayInvest HD</strong>.
      En créant un compte ou en utilisant l’application, l’utilisateur accepte
      sans réserve les présentes conditions.
    </p>

    <h2>1. Objet de l’application</h2>
    <p>
      PlayInvest HD est une application fournissant des informations financières,
      notamment des <strong>cours d’actions en temps réel</strong>, à titre
      informatif et pédagogique.
    </p>
    <p>
      L’application ne constitue en aucun cas un service de conseil financier,
      d’investissement ou de gestion de portefeuille.
    </p>

    <h2>2. Accès au service</h2>
    <p>
      L’accès à certaines fonctionnalités de l’application nécessite la création
      d’un compte utilisateur.
    </p>
    <p>
      Les informations fournies lors de la création du compte doivent être exactes,
      complètes et à jour. L’utilisateur est seul responsable des informations
      qu’il renseigne.
    </p>

    <h2>3. Compte utilisateur</h2>
    <p>
      L’utilisateur est responsable de la confidentialité de ses identifiants
      de connexion. Toute utilisation du compte est réputée effectuée par
      l’utilisateur lui-même.
    </p>
    <p>
      PlayInvest HD se réserve le droit de suspendre ou supprimer un compte en cas
      d’utilisation frauduleuse, abusive ou non conforme aux présentes conditions.
    </p>

    <h2>4. Données de marché</h2>
    <p>
      Les données de marché et cours d’actions affichés dans l’application
      proviennent de sources tierces.
      Malgré le soin apporté à leur exactitude, PlayInvest HD ne garantit pas
      l’exhaustivité, la fiabilité ou l’actualité de ces informations.
    </p>

    <h2>5. Responsabilité</h2>
    <p>
      L’utilisateur reconnaît utiliser l’application sous sa seule responsabilité.
      PlayInvest HD ne saurait être tenue responsable des décisions prises sur la
      base des informations fournies par l’application.
    </p>

    <h2>6. Propriété intellectuelle</h2>
    <p>
      L’ensemble des contenus de l’application (textes, logos, éléments graphiques,
      fonctionnalités) est protégé par le droit de la propriété intellectuelle.
      Toute reproduction ou utilisation non autorisée est interdite.
    </p>

    <h2>7. Modification des conditions</h2>
    <p>
      PlayInvest HD se réserve le droit de modifier à tout moment les présentes
      conditions d’utilisation. Les utilisateurs seront informés en cas de
      modification substantielle.
    </p>

    <h2>8. Résiliation</h2>
    <p>
      L’utilisateur peut demander la suppression de son compte à tout moment.
      PlayInvest HD se réserve également le droit de mettre fin à l’accès au
      service en cas de non-respect des présentes conditions.
    </p>

    <h2>9. Contact</h2>
    <p>
      Pour toute question concernant les présentes conditions d’utilisation :
    </p>

    <p>
      📧 <a href="mailto:contact@playinvest-hd.com">contact@playinvest-hd.com</a>
    </p>

    <p class="updated">
      Dernière mise à jour : {{ lastUpdate }}
    </p>
  </div>
</template>

<script setup>
const lastUpdate = '27 janvier 2026'
</script>

<style scoped>
.terms-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
  line-height: 1.7;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

h2 {
  margin-top: 2rem;
  font-size: 1.3rem;
}

.updated {
  margin-top: 3rem;
  font-size: 0.9rem;
  color: #666;
}
</style>
