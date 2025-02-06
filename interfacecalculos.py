import streamlit as st
from fpdf import FPDF

st.set_page_config(
    page_title='Assistente Vilma',
    page_icon='👩🏻‍💻',
)

st.sidebar.markdown('Falar com Especialista (Em construção...)')
st.sidebar.markdown('Ver vídeo de como usar (Em construção...)')

st.header('Assistente de Custos e Precificação 👩🏻‍💻')

receitas_options = [
    '',
    'Biscoitos',
    'Bolos',
    'Brigadeiros',
    'Brownies',
    'Cheesecakes',
    'Churros',
    'Cookies',
    'Cupcakes',
    'Donuts',
    'Macarons',
    'Mousse',
    'Pães doces',
    'Palha Italiana',
    'Panetone',
    'Pavê',
    'Pudim',
    'Quindim',
    'Rocambole',
    'Sonho',
    'Sorvete',
    'Tortas',
    'Trufas',
]

ingredientes_options = [
    'Açúcar',
    'Amido de milho',
    'Chocolate em pó',
    'Chocolate (barra ou gotas)',
    'Creme de leite',
    'Essência de baunilha',
    'Farinha de trigo',
    'Fermento químico',
    'Granulado',
    'Leite',
    'Leite condensado',
    'Limão',
    'Manteiga',
    'Margarina',
    'Ovos',
    'Sal',
]

embalagens_options = [
    'Caixas de papelão',
    'Caixas plástica',
    'Tapetinho',
    'Embalagem para fatia (fatia de bolo, tortas)',
    'Embalagem para Ovos de colher',
    'Embalagens para cupcakes',
    'Embalagens para doces finos',
    'Embalagens para donuts',
    'Embalagens para macarons',
    'Forminhas de papel (brigadeiro, cupcake)',
    'Forminhas de silicone',
    'Papel chumbo (para trufas e bombons)',
    'Papel manteiga',
    'Potes de acrílico',
    'Potes de isopor',
    'Potes plásticos',
    'Sacos de plástico transparente',
    'Sacos para panetone',
    'Sacos para pão doce',
]

if 'indice_ingrediente' not in st.session_state:
    st.session_state.indice_ingrediente = 0

if 'dados_ingredientes' not in st.session_state:
    st.session_state.dados_ingredientes = {}

select_receita = st.selectbox(
    label='Selecione o tipo de receita que deseja calcular',
    options=receitas_options,
)

select_ingredientes = st.multiselect(
    label='Selecione todos os ingredientes que você utilizou na receita',
    options=ingredientes_options,
)

if select_ingredientes:
    ingrediente_atual = select_ingredientes[st.session_state.indice_ingrediente]

    if ingrediente_atual not in st.session_state.dados_ingredientes:
        st.session_state.dados_ingredientes[ingrediente_atual] = {
            "quantidade_pacote": 1,  
            "valor_pacote": 0.01,  
            "quantidade_usada": 1
        }

    dados = st.session_state.dados_ingredientes[ingrediente_atual]

    st.subheader(f'Ingrediente {st.session_state.indice_ingrediente + 1}/{len(select_ingredientes)}: {ingrediente_atual}')
    quantidade_pacote = st.number_input(
        f'Quantidade do pacote de {ingrediente_atual} em gramas:',
        min_value=1, step=1, value=dados["quantidade_pacote"], key=f'quantidade_{ingrediente_atual}'
    )

    valor_pacote = st.number_input(
        f'Valor pago pelo pacote de {ingrediente_atual} R$ (PREÇO MERCADO):',
        min_value=0.01, step=0.01, value=dados["valor_pacote"], key=f'valor_{ingrediente_atual}'
    )

    quantidade_usada = st.number_input(
        f'Quantidade de {ingrediente_atual} utilizada na receita:',
        min_value=1, step=1, value=dados["quantidade_usada"], key=f'usada_{ingrediente_atual}'
    )

    st.session_state.dados_ingredientes[ingrediente_atual] = {
        'quantidade_pacote': quantidade_pacote,
        'valor_pacote': valor_pacote,
        'quantidade_usada': quantidade_usada,
    }

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Anterior", disabled=st.session_state.indice_ingrediente == 0):
            st.session_state.indice_ingrediente -= 1
            st.rerun()

    with col2:
        if st.button("Próximo ➡", key = 'botão proximo'):
            if st.session_state.indice_ingrediente < len(select_ingredientes) - 1:
                st.session_state.indice_ingrediente +=1
            else:
                st.session_state.fase_embalagens = True
            st.rerun()

    if  st.session_state.get('fase_embalagens', False):
        st.subheader('Embalagem (PREÇO MERCADO)')
        select_embalagens = st.selectbox(
            label='Selecione as embalagens que você comprou para essa receita',
            options=embalagens_options,
        )
        valor_embalagens = st.number_input(
            f'Valor pago pelo pacote de embalagens (R$):',
            min_value=0.01, step=0.01
        )
        quantidade_embalagens = st.number_input(
            f'Quantidade em unidades no pacote:',
            min_value=1, step=1
        )
        embalagem_usada = st.number_input(
            f'Quantidade em unidades usadas para a sua receita:',
            min_value=1, step=1
        )
    
        

        if st.button("Próximo ➡", key = 'botao_rendimento'):
            st.session_state.fase_rendimento = True
            st.rerun()


        if st.session_state.get('fase_rendimento', False):
            st.subheader('Rendimento da receita')
            rendimento = st.number_input(
                f'Qual foi o rendimento da sua receita de {select_receita}?',
                min_value=1, step=1
            )

        
        if st.button('Finalizar e exibir resultados'):
            st.session_state.exibir_resultados = True


        if st.session_state.get('exibir_resultados', False):
               
            custo_producao = (quantidade_usada / quantidade_pacote) * valor_pacote
            custo_embalagem = (valor_embalagens / quantidade_embalagens) * embalagem_usada        
            custos_invisiveis_margem_baixa = (custo_producao + custo_embalagem) * 0.1
            custo_total = (custo_producao + custo_embalagem + custos_invisiveis_margem_baixa)
            custo_unidade = (custo_total / rendimento)
            preco_total_margem_baixa = (custo_total * 1.5)
            preco_venda_unidade_baixa = (preco_total_margem_baixa / rendimento)
            lucro_unidade_baixa = (preco_venda_unidade_baixa - custo_unidade)
                
            custo_producao = (quantidade_usada / quantidade_pacote) * valor_pacote
            custo_embalagem = (valor_embalagens / quantidade_embalagens) * embalagem_usada        
            custos_invisiveis_margem_media = (custo_producao + custo_embalagem) * 0.15
            custo_total = (custo_producao + custo_embalagem + custos_invisiveis_margem_media)
            custo_unidade = (custo_total / rendimento)
            preco_total_margem_media = (custo_total * 2)
            preco_venda_unidade_media = (preco_total_margem_media / rendimento)
            lucro_unidade_media = (preco_venda_unidade_media - custo_unidade)
                
            custo_producao = (quantidade_usada / quantidade_pacote) * valor_pacote
            custo_embalagem = (valor_embalagens / quantidade_embalagens) * embalagem_usada        
            custos_invisiveis_margem_alta = (custo_producao + custo_embalagem) * 0.2
            custo_total = (custo_producao + custo_embalagem + custos_invisiveis_margem_alta)
            custo_unidade = (custo_total / rendimento)
            preco_total_margem_alta = (custo_total * 2.5)
            preco_venda_unidade_alta = (preco_total_margem_alta / rendimento)
            lucro_unidade_alta = (preco_venda_unidade_alta - custo_unidade)



            if st.session_state.get('exibir_resultados', False):

                resumo_relatorio = f"""
            ### | RESUMO DA RECEITA DE {select_receita.upper()} |\n

            #### MARGEM BAIXA DE 50%\n
            - Rendimento da receita: {rendimento}\n
            - Custo da produção: R$ {custo_producao:.2f}\n
            - Custo embalagem: R$ {custo_embalagem:.2f}\n
            - Custos invisíveis: R$ {custos_invisiveis_margem_baixa:.2f}\n  
            - Custo total: R$ {custo_producao + custo_embalagem + custos_invisiveis_margem_baixa:.2f}\n
            - Custo de produção por unidade: R$ {custo_unidade:.2f}\n
            - Preço venda receita completa: R$ {preco_total_margem_baixa:.2f}\n  
            - Preço venda por unidade: R$ {preco_venda_unidade_baixa:.2f}\n 
            - Lucro por unidade vendida: R$ {lucro_unidade_baixa:.2f}\n  

            #### MARGEM MÉDIA DE 100%\n  
            - Rendimento da receita: {rendimento}\n  
            - Custo da produção: R$ {custo_producao:.2f}\n  
            - Custo embalagem: R$ {custo_embalagem:.2f}\n  
            - Custos invisíveis: R$ {custos_invisiveis_margem_media:.2f}\n  
            - Custo total: R$ {custo_producao + custo_embalagem + custos_invisiveis_margem_media:.2f}\n  
            - Custo de produção por unidade: R$ {custo_unidade:.2f}\n  
            - Preço venda receita completa: R$ {preco_total_margem_media:.2f}\n 
            - Preço venda por unidade: R$ {preco_venda_unidade_media:.2f}\n  
            - Lucro por unidade vendida: R$ {lucro_unidade_media:.2f}\n  

            #### MARGEM ALTA DE 150%\n  
            - Rendimento da receita: {rendimento}\n  
            - Custo da produção: R$ {custo_producao:.2f}\n  
            - Custo embalagem: R$ {custo_embalagem:.2f}\n  
            - Custos invisíveis: R$ {custos_invisiveis_margem_alta:.2f}\n  
            - Custo total: R$ {custo_producao + custo_embalagem + custos_invisiveis_margem_alta:.2f}\n 
            - Custo de produção por unidade: R$ {custo_unidade:.2f}\n  
            - Preço venda receita completa: R$ {preco_total_margem_alta:.2f}\n  
            - Preço venda por unidade: R$ {preco_venda_unidade_alta:.2f}\n   
            - Lucro por unidade vendida: R$ {lucro_unidade_alta:.2f}\n  
            """

                st.markdown(resumo_relatorio, unsafe_allow_html=True)

                
                def generate_pdf(content):

                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)

                    pdf.multi_cell(0, 10, txt=content)
                    pdf.output("resumo_receita.pdf")

                content = resumo_relatorio

                if st.button("Gerar PDF"):
                    generate_pdf(content)
                    st.success("Gerado resumo da receita!")

                try:

                    with open("resumo_receita.pdf", "rb") as f:
                        st.download_button("Baixar PDF", f, "resumo_receita.pdf")

                except FileNotFoundError:
                    st.error("Erro: O arquivo PDF não foi gerado. Tente novamente.")


                    




