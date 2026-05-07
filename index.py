import discord
import os  # on importe les modules os et discord
from dotenv import load_dotenv  # à partir de dotenv on importe load_dotenv
load_dotenv()  # on invoque les conditions .env
bot = discord.Bot()  # on déclare le bot Discord


@bot.event  # évènement bot
async def on_ready():  # dès lors que le bot est "prêt"
    print(f"{bot.user} en ligne")  # afficher ce message dans la console

joueur_pseudo, joueur_inviteur, partie_on, joueur_deno, gagnant = "", "", False, True, "" # def des variables
tableau = [["<:gris:1084123301363851264>" for x in range(7)] for n in range(6)]  # def du tableau


async def display(interaction):  # Fonction pour afficher le tableau
    global tableau
    #   Affichage du tableau
    tableau_embed = ":one: :two: :three: :four: :five: :six: :seven:\n\n" \
                    f"{tableau[0][0]} {tableau[0][1]} {tableau[0][2]} {tableau[0][3]} {tableau[0][4]} {tableau[0][5]} {tableau[0][6]}\n" \
                    f"{tableau[1][0]} {tableau[1][1]} {tableau[1][2]} {tableau[1][3]} {tableau[1][4]} {tableau[1][5]} {tableau[1][6]}\n" \
                    f"{tableau[2][0]} {tableau[2][1]} {tableau[2][2]} {tableau[2][3]} {tableau[2][4]} {tableau[2][5]} {tableau[2][6]}\n" \
                    f"{tableau[3][0]} {tableau[3][1]} {tableau[3][2]} {tableau[3][3]} {tableau[3][4]} {tableau[3][5]} {tableau[3][6]}\n" \
                    f"{tableau[4][0]} {tableau[4][1]} {tableau[4][2]} {tableau[4][3]} {tableau[4][4]} {tableau[4][5]} {tableau[4][6]}\n" \
                    f"{tableau[5][0]} {tableau[5][1]} {tableau[5][2]} {tableau[5][3]} {tableau[5][4]} {tableau[5][5]} {tableau[5][6]}\n"
    embed = discord.Embed(  # définition de l'embed (de l'affichage)
        title="Puissance 4",
        description=tableau_embed,
        color=discord.Colour.blue(),
    )
    if gagnant == "<:rouge:1084123220128575518>":  # si gagnant est rouge
        embed.add_field(name="PARTIE TERMINEE", value=f"{joueur_pseudo} <:rouge:1084123220128575518> a gagné.e la partie !")  # on ajoute un field à l'embed
        await partieFin(interaction, embed)
        return
    elif gagnant == "<:jaune:1084132128167563354>":  # si gagnant est jaune, idem qu'en haut
        embed.add_field(name="PARTIE TERMINEE", value=f"{joueur_inviteur} <:jaune:1084132128167563354> a gagné.e la partie !")
        await partieFin(interaction, embed)
        return
    elif gagnant == "plein":  # si le tableau est plein, idem qu'en haut
        embed.add_field(name="PARTIE TERMINEE", value="Le tableau est plein ! match nul")
        await partieFin(interaction, embed)
        return
    if not joueur_deno:  # si le joueur n'est pas le joueur dominé
        embed.add_field(name="Joueurs", value=f"{joueur_inviteur} <:jaune:1084132128167563354> **c'est à toi**\n{joueur_pseudo} <:rouge:1084123220128575518>")  # on modifie l'embed avec le joueur
    else:  # sinon idem
        embed.add_field(name="Joueurs", value=f"{joueur_inviteur} <:jaune:1084132128167563354>\n{joueur_pseudo} <:rouge:1084123220128575518> **c'est à toi**")
    await interaction.response.edit_message(content="", embed=embed, view=Boutons1())  # on met à jour l'interaction avec les boutons de la classe Boutons1


async def partieFin(interaction, embed):
    global partie_on, tableau, gagnant, joueur_deno
    await interaction.response.edit_message(content="", embed=embed, view=Fin())
    tableau = [["<:gris:1084123301363851264>" for x in range(7)] for n in range(6)]
    gagnant = ""
    partie_on = False
    joueur_deno = True


async def insertJeton(colonne: int, jeton: str):  # Fonction pour insérer un jeton
    global joueur_deno, gagnant
    ligne = len(tableau) - 1  # On détermine les lignes du tableau

    while ligne >= 0:  # si ligne est supérieure à 0
        if tableau[ligne][colonne] != "<:gris:1084123301363851264>":  # si ligne n'est pas vide
            ligne = ligne - 1  # on recule d'une ligne
        else:  # sinon
            tableau[ligne][colonne] = jeton  # on met un jeton
            break

    # diagonale droit
    for col in range(4):
        for row in range(3):  # ligne de bas en haut
            if tableau[row][col] == jeton and tableau[row+1][col+1] == jeton and tableau[row+2][col+2] == jeton and tableau[row+3][col+3] == jeton:
                if jeton == "<:jaune:1084132128167563354>":
                    tableau[row][col] = "<:jaunewin:1086260143324405851>"; tableau[row+1][col+1] = "<:jaunewin:1086260143324405851>"; tableau[row+2][col+2] = "<:jaunewin:1086260143324405851>"; tableau[row+3][col+3] = "<:jaunewin:1086260143324405851>"
                else:
                    tableau[row][col] = "<:rougewin:1086260115344211979>"; tableau[row+1][col+1] = "<:rougewin:1086260115344211979>"; tableau[row+2][col+2] = "<:rougewin:1086260115344211979>"; tableau[row+3][col+3] = "<:rougewin:1086260115344211979>"
                gagnant = jeton
    # diagonale gauche
    for col in range(3, 6):
        for row in range(3):
            if tableau[row][col] == jeton and tableau[row+1][col-1] == jeton and tableau[row+2][col-2] == jeton and tableau[row+3][col-3] == jeton:
                if jeton == "<:jaune:1084132128167563354>":
                    tableau[row][col] = "<:jaunewin:1086260143324405851>"; tableau[row+1][col-1] = "<:jaunewin:1086260143324405851>"; tableau[row+2][col-2] = "<:jaunewin:1086260143324405851>"; tableau[row+3][col-3] = "<:jaunewin:1086260143324405851>"
                else:
                    tableau[row][col] = "<:rougewin:1086260115344211979>"; tableau[row+1][col-1] = "<:rougewin:1086260115344211979>"; tableau[row+2][col-2] = "<:rougewin:1086260115344211979>"; tableau[row+3][col-3] = "<:rougewin:1086260115344211979>"
                gagnant = jeton
    # vertical
    for col in range(7):
        for row in range(3):
            if tableau[row][col] == jeton and tableau[row+1][col] == jeton and tableau[row+2][col] == jeton and tableau[row+3][col] == jeton:
                if jeton == "<:jaune:1084132128167563354>":
                    tableau[row][col] = "<:jaunewin:1086260143324405851>"; tableau[row+1][col] = "<:jaunewin:1086260143324405851>"; tableau[row+2][col] = "<:jaunewin:1086260143324405851>"; tableau[row+3][col] = "<:jaunewin:1086260143324405851>"
                else:
                    tableau[row][col] = "<:rougewin:1086260115344211979>"; tableau[row+1][col] = "<:rougewin:1086260115344211979>"; tableau[row+2][col] = "<:rougewin:1086260115344211979>"; tableau[row+3][col] = "<:rougewin:1086260115344211979>"
                gagnant = jeton

    # horizontal
    for col in range(4):
        for row in range(6):
            if tableau[row][col] == jeton and tableau[row][col+1] == jeton and tableau[row][col+2] == jeton and tableau[row][col+3] == jeton:
                if jeton == "<:jaune:1084132128167563354>":
                    tableau[row][col] = "<:jaunewin:1086260143324405851>"; tableau[row][col+1] = "<:jaunewin:1086260143324405851>"; tableau[row][col+2] = "<:jaunewin:1086260143324405851>"; tableau[row][col+3] = "<:jaunewin:1086260143324405851>"
                else:
                    tableau[row][col] = "<:rougewin:1086260115344211979>"; tableau[row][col+1] = "<:rougewin:1086260115344211979>"; tableau[row][col+2] = "<:rougewin:1086260115344211979>"; tableau[row][col+3] = "<:rougewin:1086260115344211979>"
                gagnant = jeton


class Boutons(discord.ui.View):  # on définit la classe Boutons de départ (annuler, accepter)

    @discord.ui.button(label="Accepter", custom_id="button-1", style=discord.ButtonStyle.success)  # on invoque l'évènement du bouton avec ses infos
    async def first_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        global joueur_pseudo, partie_on, joueur_deno
        if joueur_pseudo != interaction.user:  # si la personne qui a interagit avec le bouton n'est pas le joueur invité
            await interaction.response.send_message("Tu n'as pas la permission d'accepter l'invitation", ephemeral=True) # on répond en masqué à l'utilisateur
        else:  # sinon
            await display(interaction)  # on affiche le tableau
            partie_on = True  # on définit qu'une partie est en cours

    @discord.ui.button(label="Annuler", custom_id="button-2", style=discord.ButtonStyle.secondary)  # on invoque l'évènement du bouton avec ses infos
    async def second_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        global joueur_pseudo, partie_on, joueur_inviteur
        if interaction.user == joueur_pseudo or interaction.user == joueur_inviteur:  # si la personne qui interagit avec le bouton est le joueur invité ou inviteur
            await interaction.response.edit_message(content=f"Partie annulée par {interaction.user}", view=Fin())  # on modifie l'interaction et on met fin au jeu
            partie_on = False
        else:
            await interaction.response.send_message("Tu n'as pas la permission d'annuler l'invitation", ephemeral=True)  # sinon on affiche en masqué ceci


async def denomination(jeton, interaction: discord.Interaction):  # fonction dénomination
    global joueur_deno, joueur_pseudo, joueur_inviteur, gagnant
    if joueur_deno:  # si c'est le joueur dénominé
        if interaction.user == joueur_pseudo:  # si la personne qui a interagie est le joueur invité
            if tableau[0][0] != "<:gris:1084123301363851264>" and tableau[0][1] != "<:gris:1084123301363851264>" and tableau[0][2] != "<:gris:1084123301363851264>" and tableau[0][3] != "<:gris:1084123301363851264>" and tableau[0][4] != "<:gris:1084123301363851264>" and tableau[0][5] != "<:gris:1084123301363851264>" and tableau[0][6] != "<:gris:1084123301363851264>":
                gagnant = "plein"  # si tableau plein on change le contenu de "gagnant"
            elif tableau[0][jeton] != "<:gris:1084123301363851264>":  # sinon si la colonne est pleine
                await interaction.response.send_message(content=f"La colonne {jeton} est pleine !", ephemeral=True)  # on affiche en masqué ceci
            else:  # sinon
                await insertJeton(jeton, "<:rouge:1084123220128575518>")  # on insère le jeton
                joueur_deno = False  # on change de joueur
                await display(interaction)  # on affiche le tableau
        else:
            await interaction.response.send_message(content="Ce n'est pas ton tour", ephemeral=True)  # sinon on refuse l'autre joueur de jouer
    else:  # sinon (idem pour les commentaires d'haut dessus)
        if interaction.user == joueur_inviteur:
            if tableau[0][0] != "<:gris:1084123301363851264>" and tableau[0][1] != "<:gris:1084123301363851264>" and tableau[0][2] != "<:gris:1084123301363851264>" and tableau[0][3] != "<:gris:1084123301363851264>" and tableau[0][4] != "<:gris:1084123301363851264>" and tableau[0][5] != "<:gris:1084123301363851264>" and tableau[0][6] != "<:gris:1084123301363851264>":
                gagnant = "plein"
            elif tableau[0][jeton] != "<:gris:1084123301363851264>":
                await interaction.response.send_message(content=f"La colonne {jeton} est pleine !", ephemeral=True)
            else:
                await insertJeton(jeton, "<:jaune:1084132128167563354>")
                joueur_deno = True
                await display(interaction)
        else:
            await interaction.response.send_message(content="Ce n'est pas ton tour", ephemeral=True)


class Fin(discord.ui.View):  # classe de Fin pour arrêter d'afficher les boutons
    pass


class Boutons1(discord.ui.View):  # classe Boutons1 pour afficher les boutons de colonne

    @discord.ui.button(emoji="1️⃣", custom_id="button-0.1", row=0, style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def zero_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(0, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(emoji="2️⃣", row=0, custom_id="button-1.1", style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def one_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(1, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(emoji="3️⃣", row=0, custom_id="button-2.1", style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def two_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(2, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(emoji="4️⃣", row=0, custom_id="button-3.1", style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def three_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(3, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(emoji="5️⃣", row=1, custom_id="button-4.1", style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def four_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(4, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(emoji="6️⃣", row=1, custom_id="button-5.1", style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def five_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(5, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(emoji="7️⃣", row=1, custom_id="button-6.1", style=discord.ButtonStyle.secondary) # on invoque l'évènement du bouton avec ses infos
    async def six_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        await denomination(6, interaction)  # on fait appel à dénomination en fonction de la colonne

    @discord.ui.button(label="Arrêter", row=1, custom_id="button-stop", style=discord.ButtonStyle.danger) # on invoque l'évènement du bouton avec ses infos
    async def seven_button_callback(self, button, interaction: discord.Interaction):  # fonction du bouton
        global partie_on, tableau
        if interaction.user == joueur_pseudo or interaction.user == joueur_inviteur:  # si la personne qui a interagit avec le bouton est le joueur invité ou inviteur
            await interaction.message.edit(content=f"Jeu arrêté par {interaction.user}", embed=None, view=Fin())  # on modifie l'interaction et on met fin à la partie
            partie_on = False  # on passe la valeur à false pour pouvoir refaire une partie
            tableau = [["<:gris:1084123301363851264>" for x in range(7)] for n in range(6)]
        else:
            await interaction.response.send_message(content="Tu n'as pas la permission d'arrêter la partie", ephemeral=True)  # sinon, on refuse la personne d'arrêter la partie


@bot.slash_command(name="puissance4", description="Joue au puissance 4 avec un ami")  # évènement pour les commandes slash
async def puissance_4(ctx: discord.ApplicationContext, joueur: discord.Option(discord.User, required=True, description="Choisir un joueur")):  # fonction puissance_4 pour la commande avec ses infos
    global joueur_pseudo, partie_on, joueur_inviteur
    if partie_on:  # si partie_on est sur True
        await ctx.respond("Une partie est déjà en cours", ephemeral=True)
    elif joueur == ctx.user:  # Sinon si le joueur dominé est le joueur lui-même
        await ctx.respond("Tu ne peux pas jouer avec toi-même !", ephemeral=True)
    elif joueur.bot:  # si le joueur dénominé est un bot
        await ctx.respond("Tu ne peux pas jouer avec un bot !", ephemeral=True)
    else:  # sinon
        joueur_pseudo = joueur  # on définit joueur_pseudo comme le joueur invité
        joueur_inviteur = ctx.user  # et joueur_inviteur comme l'inviteur
        await ctx.respond(f'{joueur.mention}, veux-tu jouer au puissance 4 avec {ctx.user.mention} ?', view=Boutons())  # on envoie la requête de demande de jeu
bot.run(os.getenv('TOKEN'))  # on démarre le bot grâce à son jeton de connexion via le fichier .env
